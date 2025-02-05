from usdm_model.identifier import StudyIdentifier
from usdm_model.organization import Organization
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.globals import Globals


class StudyIdentifiersSheet(BaseSheet):
    SHEET_NAME = "studyIdentifiers"

    def __init__(self, file_path, globals: Globals):
        try:
            self.items = []
            super().__init__(
                file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME
            )
            self._process_sheet()
        except Exception as e:
            self._sheet_exception(e)

    def _process_sheet(self):
        for index, row in self.sheet.iterrows():
            org_name = self.read_cell_by_name(index, "organization")
            organization: Organization = self.globals.cross_references.get(
                Organization, org_name
            )
            if organization:
                item: StudyIdentifier = self.create_object(
                    StudyIdentifier,
                    {
                        "text": self.read_cell_by_name(
                            index, ["studyIdentifier", "identifier"]
                        ),
                        "scopeId": organization.id,
                    },
                )
                if item:
                    self.items.append(item)
                    self.globals.cross_references.add(item.text, item)
            else:
                self._error(
                    index,
                    "organization",
                    f"Failed to find organization with name '{org_name}'",
                )
