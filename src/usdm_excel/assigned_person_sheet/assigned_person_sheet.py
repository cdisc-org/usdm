from usdm_excel.base_sheet import BaseSheet
from usdm_model.assigned_person import AssignedPerson
from usdm_model.organization import Organization
from usdm_excel.globals import Globals


class AssignedPersonSheet(BaseSheet):
    SHEET_NAME = "people"

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
                    params = {
                        "name": self.read_cell_by_name(index, "name"),
                        "description": self.read_cell_by_name(
                            index, "description", default=""
                        ),
                        "label": self.read_cell_by_name(index, "label", default=""),
                        "personName": self.read_person_name_cell_by_name(
                            index, "personName"
                        ),
                        "jobTitle": self.read_cell_by_name(index, "jobTitle"),
                        "organizationId": self._get_org(index),
                    }
                    item = self.create_object(AssignedPerson, params)
                    if item:
                        self.items.append(item)
                        self.globals.cross_references.add(item.name, item)
        except Exception as e:
            self._sheet_exception(e)

    def _get_org(self, index: int) -> str:
        org_ref = self.read_cell_by_name(index, "organization", default="")
        org = (
            self.globals.cross_references.get(Organization, org_ref)
            if org_ref
            else None
        )
        return org.id if org else None
