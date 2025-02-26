from .utility import usdm_reference
from usdm_model.study_version import StudyVersion
from usdm_model.study_definition_document_version import StudyDefinitionDocumentVersion
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.document.elements import Elements


class TemplateBase:
    def __init__(
        self,
        parent: BaseSheet,
        study_version: StudyVersion,
        document_version: StudyDefinitionDocumentVersion,
    ):
        self.parent = parent
        self._study_version = study_version
        self._study_design = self._study_version.studyDesigns[0]
        self._document_version = document_version
        self._elements = Elements(parent, study_version, document_version)
        self._methods = [
            func
            for func in dir(self.__class__)
            if callable(getattr(self.__class__, func)) and not func.startswith("_")
        ]

    def valid_method(self, name):
        result = name in self._methods
        if not result:
            self.parent._general_warning(
                f"Could not resolve method name, {name} not in {self._methods}"
            )
        return result

    def _reference(self, item, attribute):
        return usdm_reference(item, attribute)

    def _add_checking_for_tag(self, doc, tag, text):
        doc.asis(text)

    def _critierion_item(self, item_id):
        return next(
            (
                x
                for x in self._study_version.eligibilityCriterionItems
                if x.id == item_id
            ),
            None,
        )
