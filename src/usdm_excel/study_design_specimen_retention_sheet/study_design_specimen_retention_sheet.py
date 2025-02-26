from usdm_model.biospecimen_retention import BiospecimenRetention
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.globals import Globals


class StudyDesignSpecimenRetentionSheet(BaseSheet):
    SHEET_NAME = "studyDesignSpecimen"

    def __init__(self, file_path, globals: Globals):
        try:
            self.items = []
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=self.SHEET_NAME,
                optional=True,
            )
            if self.success:
                self._process_sheet()
        except Exception as e:
            self._sheet_exception(e)

    def _process_sheet(self):
        for index, row in self.sheet.iterrows():
            name = self.read_cell_by_name(index, ["name"])
            description = self.read_cell_by_name(
                index, "description", default="", must_be_present=False
            )
            label = self.read_cell_by_name(
                index, "label", default="", must_be_present=False
            )
            retained = self.read_boolean_cell_by_name(index, "retained")
            includesDNA = self.read_boolean_cell_by_name(index, "includesDNA")
            item: BiospecimenRetention = self.create_object(
                BiospecimenRetention,
                {
                    "name": name,
                    "description": description,
                    "label": label,
                    "isRetained": retained,
                    "includesDNA": includesDNA,
                },
            )
            if item:
                self.globals.cross_references.add(item.name, item)
                self.items.append(item)
