from usdm_model.wrapper import Wrapper
from usdm_model.study import Study
from usdm_model.study_design import StudyDesign
from usdm_model.study_version import StudyVersion
from usdm_model.study_title import StudyTitle
from usdm_model.study_definition_document import StudyDefinitionDocument
from usdm_model.study_definition_document_version import StudyDefinitionDocumentVersion
from usdm_model.code import Code
from usdm_model.identifier import StudyIdentifier
from usdm_model.organization import Organization
from usdm_model.address import Address
from usdm_model.narrative_content import NarrativeContent
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging
from usdm_excel.id_manager import IdManager
from usdm_excel.cdisc_ct_library import CDISCCTLibrary
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.composition import Composition, CompositionSection
from uuid import uuid4
from usdm_info import (
    __model_version__ as usdm_version,
    __package_version__ as system_version,
)


class FromFHIR:
    SYSTEM_NAME = "CDISC USDM FHIR"

    class LogicError(Exception):
        pass

    def __init__(self, errors_and_logging: ErrorsAndLogging):
        self._errors_and_logging = ErrorsAndLogging()
        self._id_manager = IdManager(self._errors_and_logging)
        self._cdisc_ct_manager = CDISCCTLibrary(self._errors_and_logging)

    def from_fhir(self, data: str) -> Wrapper:
        try:
            bundle = Bundle.parse_raw(data)
            study = self._study(bundle.entry[0].resource.title)
            doc_version = self._document_version(study)
            root = self._model_instance(
                NarrativeContent,
                {
                    "name": "ROOT",
                    "sectionNumber": "0",
                    "sectionTitle": "Root",
                    "text": "",
                    "childIds": [],
                    "previousId": None,
                    "nextId": None,
                },
            )
            doc_version.contents.append(root)
            for item in bundle.entry[0].resource.section:
                nc_item = self._section(item, doc_version)
                root.childIds.append(nc_item.id)
            self._double_link(doc_version.contents, "previousId", "nextId")
            return Wrapper(
                study=study,
                usdmVersion=usdm_version,
                systemName=self.SYSTEM_NAME,
                systemVersion=system_version,
            )
        except Exception as e:
            self._errors_and_logging.exception(
                f"Exception raised parsing FHIR content. See logs for more details", e
            )
            return None

    def _section(self, section: CompositionSection, doc_version):
        print(f"SECTION: {section.title}, {section.code.text}")
        nc = self._model_instance(
            NarrativeContent,
            {
                "name": f"{section.code.text}",
                "sectionNumber": "",
                "sectionTitle": section.title,
                "text": section.text.div,
                "childIds": [],
                "previousId": None,
                "nextId": None,
            },
        )
        doc_version.contents.append(nc)
        if section.section:
            for item in section.section:
                item_nc = self._section(item, doc_version)
                nc.childIds.append(item_nc.id)
        return nc

    def _study(self, title):
        sponsor_title_code = self._cdisc_ct_code("C99905x2", "Official Study Title")
        protocl_status_code = self._cdisc_ct_code("C85255", "Draft")
        intervention_model_code = self._cdisc_ct_code("C82639", "Parallel Study")
        country_code = self._iso_country_code("DNK", "Denmark")
        sponsor_code = self._cdisc_ct_code("C70793", "Clinical Study Sponsor")
        study_title = self._model_instance(
            StudyTitle, {"text": title, "type": sponsor_title_code}
        )
        protocl_document_version = self._model_instance(
            StudyDefinitionDocumentVersion,
            {"protocolVersion": "1", "protocolStatus": protocl_status_code},
        )
        protocl_document = self._model_instance(
            StudyDefinitionDocument,
            {
                "name": "PROTOCOL V1",
                "label": "",
                "description": "",
                "versions": [protocl_document_version],
            },
        )
        study_design = self._model_instance(
            StudyDesign,
            {
                "name": "Study Design",
                "label": "",
                "description": "",
                "rationale": "XXX",
                "interventionModel": intervention_model_code,
                "arms": [],
                "studyCells": [],
                "epochs": [],
                "population": None,
            },
        )
        address = self._model_instance(
            Address,
            {
                "line": "Den Lille Havfrue",
                "city": "Copenhagen",
                "district": "",
                "state": "",
                "postalCode": "12345",
                "country": country_code,
            },
        )
        organization = self._model_instance(
            Organization,
            {
                "name": "Sponsor",
                "organizationType": sponsor_code,
                "identifier": "123456789",
                "identifierScheme": "DUNS",
                "legalAddress": address,
            },
        )
        identifier = self._model_instance(
            StudyIdentifier, {"text": "SPONSOR-1234", "scope": organization}
        )
        study_version = self._model_instance(
            StudyVersion,
            {
                "versionIdentifier": "1",
                "rationale": "XXX",
                "titles": [study_title],
                "studyDesigns": [study_design],
                "documentVersionId": protocl_document_version.id,
                "studyIdentifiers": [identifier],
            },
        )
        study = self._model_instance(
            Study,
            {
                "id": uuid4(),
                "name": "Study",
                "label": "",
                "description": "",
                "versions": [study_version],
                "documentedBy": protocl_document,
            },
        )
        return study

    def _cdisc_ct_code(self, code, decode):
        return self._model_instance(
            Code,
            {
                "code": code,
                "decode": decode,
                "codeSystem": self._cdisc_ct_manager.system,
                "codeSystemVersion": self._cdisc_ct_manager.version,
            },
        )

    def _iso_country_code(self, code, decode):
        return self._model_instance(
            Code,
            {
                "code": code,
                "decode": decode,
                "codeSystem": "ISO 3166 1 alpha3",
                "codeSystemVersion": "2020-08",
            },
        )

    def _document_version(self, study):
        return study.documentedBy.versions[0]

    def _model_instance(self, cls, params):
        params["id"] = (
            params["id"] if "id" in params else self._id_manager.build_id(cls)
        )
        params["instanceType"] = cls.__name__
        return cls(**params)

    def _double_link(self, items, prev, next):
        for idx, item in enumerate(items):
            if idx == 0:
                setattr(item, prev, None)
            else:
                the_id = getattr(items[idx - 1], "id")
                setattr(item, prev, the_id)
            if idx == len(items) - 1:
                setattr(item, next, None)
            else:
                the_id = getattr(items[idx + 1], "id")
                setattr(item, next, the_id)
