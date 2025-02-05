from usdm_model.identifier import ReferenceIdentifier
from usdm_model.organization import Organization
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.globals import Globals


class StudyReferencesSheet(BaseSheet):
    SHEET_NAME = "studyReferences"

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
            text = self.read_cell_by_name(index, ["studyIdentifier", "identifier"])
            org_name = self.read_cell_by_name(index, "organization")
            type = self.read_cdisc_klass_attribute_cell_by_name(
                "ReferenceIdentifier", "type", index, ["referenceType", "type"]
            )
            organization = self.globals.cross_references.get(Organization, org_name)
            if organization:
                item = self.create_object(
                    ReferenceIdentifier,
                    {"text": text, "type": type, "scopeId": organization.id},
                )
                if item:
                    self.items.append(item)
                    self.globals.cross_references.add(item.text, item)
            else:
                self._error(
                    row,
                    "organization",
                    f"Failed to find organization with name '{org_name}'",
                )
