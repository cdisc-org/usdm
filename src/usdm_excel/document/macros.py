import os
import base64
from usdm_excel.document.template_m11 import TemplateM11
from usdm_excel.document.template_plain import TemplatePlain
from usdm_excel.document.elements import Elements
from usdm_excel.base_sheet import BaseSheet
from usdm_model.abbreviation import Abbreviation
from usdm_model.study_version import StudyVersion
from usdm_model.study_definition_document_version import StudyDefinitionDocumentVersion
from usdm_model.activity import Activity
from usdm_model.biomedical_concept import BiomedicalConcept
from usdm_model.biomedical_concept_surrogate import BiomedicalConceptSurrogate
from usdm_excel.document.utility import get_soup


class Macros:
    def __init__(
        self,
        parent: BaseSheet,
        study_version: StudyVersion,
        document_version: StudyDefinitionDocumentVersion,
    ):
        self._parent = parent
        self._study_version = study_version
        self._study_design = self._study_version.studyDesigns[0]
        self._document_version = document_version

        self._elements = Elements(parent, study_version, document_version)
        self._m11 = TemplateM11(parent, study_version, document_version)
        self._plain = TemplatePlain(parent, study_version, document_version)
        self._template_map = {"m11": self._m11, "plain": self._plain}

    def resolve(self, content_text: str) -> str:
        soup = get_soup(content_text, self._parent)
        for ref in soup(["usdm:macro"]):
            try:
                attributes = ref.attrs
                method = f"_{attributes['id'].lower()}"
                if self._valid_method(method):
                    result = getattr(self, method)(attributes, soup, ref)
                else:
                    self._parent._general_error(
                        f"Failed to resolve document macro '{attributes}', invalid method name {method}"
                    )
                    ref.replace_with("Missing content: invalid method name")
            except Exception as e:
                self._parent._general_exception(
                    f"Failed to resolve document macro '{attributes}'", e
                )
                ref.replace_with("Missing content: exception")
        return str(soup)

    def _xref(self, attributes: dict, soup, ref) -> None:
        instance, attribute = self._parent.globals.cross_references.get_by_path(
            attributes["klass"], attributes["name"], attributes["attribute"]
        )
        ref_tag = soup.new_tag("usdm:ref")
        ref_tag.attrs = {
            "klass": instance.__class__.__name__,
            "id": instance.id,
            "attribute": attribute,
        }
        ref.replace_with(ref_tag)

    def _abbreviations(self, attributes: dict, soup, ref) -> None:
        items = [x.strip() for x in attributes["items"].split(",")]
        separator = attributes["separator"] if "separator" in attributes else ","
        first = True
        for item in items:
            instance = self._parent.globals.cross_references.get(Abbreviation, item)
            if instance:
                if not first:
                    ref.insert_before(f"{separator} ")
                ref.insert_before(
                    self._new_ref_tag(
                        soup, "Abbreviation", instance.id, "abbreviatedText"
                    )
                )
                ref.insert_before(" = ")
                ref.insert_before(
                    self._new_ref_tag(soup, "Abbreviation", instance.id, "expandedText")
                )
                first = False
            else:
                self._parent._general_error(f"Failed to find abbreviation '{item}'")
                ref.insert_after(
                    f"Missing abbreviation: failed to find abbreviation '{item}'"
                )
        ref.extract()

    def _new_ref_tag(self, soup, klass: str, id: str, attribute: str):
        tag = soup.new_tag("usdm:ref")
        tag.attrs = {"klass": klass, "id": id, "attribute": attribute}
        return tag

    def _bc(self, attributes: dict, soup, ref) -> None:
        bc_name = attributes["name"].upper().strip()
        activity_name = attributes["activity"].strip()
        activity = self._parent.globals.cross_references.get(Activity, activity_name)
        if activity:
            bc = None
            for collection in [
                {
                    "klass": BiomedicalConcept,
                    "ids": activity.biomedicalConceptIds,
                    "synonyms": True,
                },
                {
                    "klass": BiomedicalConceptSurrogate,
                    "ids": activity.bcSurrogateIds,
                    "synonyms": False,
                },
            ]:
                for id in collection["ids"]:
                    next_bc = self._parent.globals.cross_references.get_by_id(
                        collection["klass"], id
                    )
                    if next_bc:
                        if bc_name == next_bc.name.upper() or bc_name in [
                            x.upper() for x in next_bc.synonyms
                        ]:
                            bc = next_bc
                            break
            if bc:
                ref_tag = soup.new_tag("usdm:ref")
                ref_tag.attrs = {
                    "klass": bc.__class__.__name__,
                    "id": bc.id,
                    "attribute": "label",
                }
                ref.replace_with(ref_tag)
            else:
                self._parent._general_error(
                    f"Failed to find BC name '{bc_name}' in activity '{activity_name}'"
                )
                ref.replace_with("Missing BC: failed to find BC in activity")
        else:
            self._parent._general_error(f"Failed to find activity '{activity_name}'")
            ref.replace_with(
                f"Missing activity: failed to find activity '{activity_name}'"
            )

    def _image(self, attributes: dict, soup, ref) -> None:
        type = attributes["type"]
        data = self._encode_image(attributes["file"])
        if data:
            img_tag = soup.new_tag("img")
            img_tag.attrs["src"] = f"data:image/{type};base64,{data.decode('ascii')}"
            img_tag.attrs["alt"] = "Alt text"
            ref.replace_with(img_tag)
        else:
            name = attributes["file"]
            self._parent._general_error(f"Failed to insert image '{name}'")
            ref.replace_with(f"Missing image: failed to insert image '{name}'")

    def _element(self, attributes, soup, ref) -> None:
        method = attributes["name"].lower()
        if self._elements.valid_method(method):
            text = getattr(self._elements, method)()
            ref.replace_with(get_soup(text, self._parent))
        else:
            self._parent._general_error(
                f"Failed to translate element method name '{method}' in '{attributes}', invalid method"
            )
            ref.replace_with("Missing content: invalid method name")

    def _section(self, attributes, soup, ref) -> None:
        method = attributes["name"].lower()
        template = attributes["template"] if "template" in attributes else "plain"
        instance = self._resolve_template(template)
        if instance.valid_method(method):
            text = getattr(instance, method)(attributes)
            ref.replace_with(get_soup(text, self._parent))
        else:
            self._parent._general_error(
                f"Failed to translate section method name '{method}' in '{attributes}', invalid method"
            )
            ref.replace_with("Missing content: invalid method name")

    def _note(self, attributes, soup, ref) -> None:
        text = f"""
      <div class="col-md-8 offset-md-2 text-center">
        <p class="usdm-warning">Note:</p>
        <p class="usdm-warning">{attributes["text"]}</p>
      </div>
    """
        ref.replace_with(get_soup(text, self._parent))

    def _valid_method(self, name):
        return name in [
            "_xref",
            "_image",
            "_element",
            "_section",
            "_note",
            "_bc",
            "_abbreviations",
        ]

    def _resolve_template(self, template: str) -> object:
        try:
            return self._template_map[template.lower()]
        except:
            self._parent._general_error(
                f"Failed to map template '{template}', using plain template"
            )
            return self._plain

    def _encode_image(self, filename: str) -> bytes:
        try:
            with open(
                os.path.join(self._parent.dir_path, filename), "rb"
            ) as image_file:
                data = base64.b64encode(image_file.read())
            return data
        except Exception as e:
            self._parent._general_exception(
                f"Failed to open / read image file '{filename}', ignored", e
            )
            return None
