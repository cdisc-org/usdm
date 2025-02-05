from usdm_excel.base_sheet import BaseSheet
from usdm_model.abbreviation import Abbreviation
from usdm_excel.globals import Globals


class AbbreviationSheet(BaseSheet):
    SHEET_NAME = "abbreviations"

    def __init__(self, file_path: str, globals: Globals):
        try:
            self.items = []
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=self.SHEET_NAME,
                optional=True,
            )
            if self.success:
                for index, row in self.sheet.iterrows():
                    abbreviation = self.read_cell_by_name(index, "abbreviatedText")
                    text = self.read_cell_by_name(index, "expandedText")
                    params = {"abbreviatedText": abbreviation, "expandedText": text}
                    notes = self.read_cell_multiple_by_name(
                        index, "notes", must_be_present=False
                    )
                    item = self.create_object(Abbreviation, params)
                    if item:
                        self.items.append(item)
                        self.globals.cross_references.add(abbreviation, item)
                        self.add_notes(item, notes)
        except Exception as e:
            self._sheet_exception(e)
