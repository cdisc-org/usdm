from usdm_excel.base_sheet import BaseSheet
from usdm_model.narrative_content import NarrativeContent, NarrativeContentItem
from usdm_model.study_version import StudyVersion
from usdm_model.study_definition_document_version import StudyDefinitionDocumentVersion
from usdm_excel.globals import Globals
from usdm_excel.document.macros import Macros


class DocumentContentSheet(BaseSheet):
    SHEET_NAME = "documentContent"
    DIV_OPEN_NS = '<div xmlns="http://www.w3.org/1999/xhtml">'
    DIV_OPEN = "<div>"
    DIV_CLOSE = "</div>"

    def __init__(self, file_path: str, globals: Globals):
        try:
            self.items = []
            self._map = {}
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=self.SHEET_NAME,
                optional=True,
            )
            if self.success:
                for index, row in self.sheet.iterrows():
                    text = self.read_cell_by_name(index, "text")
                    name = self.read_cell_by_name(index, "name")
                    item = self.create_object(
                        NarrativeContentItem,
                        {"name": name, "text": self._wrap_div(text)},
                    )
                    if item:
                        self.items.append(item)
                        self.globals.cross_references.add(name, item)
                        self._map[item.id] = item
        except Exception as e:
            self._sheet_exception(e)

    # @todo: This code should probably be elsewhere
    def resolve(
        self,
        study_version: StudyVersion,
        document_version: StudyDefinitionDocumentVersion,
    ):
        macros = Macros(self, study_version, document_version)
        for nc in document_version.contents:
            if nc.contentItemId:
                nci = self._map[nc.contentItemId]
                nci.text = macros.resolve(nci.text)

    def _wrap_div(self, text):
        if text.startswith(self.DIV_OPEN_NS):
            return text
        elif text.startswith(self.DIV_OPEN):
            return text.replace(self.DIV_OPEN, self.DIV_OPEN_NS)
        else:
            return f"{self.DIV_OPEN_NS}{text}{self.DIV_CLOSE}"
