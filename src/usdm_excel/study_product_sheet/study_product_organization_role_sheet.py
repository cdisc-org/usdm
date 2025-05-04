from usdm_excel.base_sheet import BaseSheet
from usdm_model.product_organization_role import ProductOrganizationRole
from usdm_model.organization import Organization
from usdm_excel.globals import Globals


class StudyProductOrganizationRoleSheet(BaseSheet):
    SHEET_NAME = "studyProductOrganizationRoles"

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
                        "organizationId": self.globals.cross_references.get(
                            Organization, self.read_cell_by_name(index, "organization")
                        ).id,
                        "code": self.read_cdisc_klass_attribute_cell_by_name(
                            "ProductOrganizationRole", "code", index, "role"
                        ),
                        "appliesToIds": self._process_applies_to_references(index),
                    }
                    item = self.create_object(ProductOrganizationRole, params)
                    if item:
                        self.items.append(item)
                        self.globals.cross_references.add(item.name, item)
        except Exception as e:
            self._sheet_exception(e)

    def _process_applies_to_references(self, index):
        results = []
        klasses = ["AdministrableProduct", "MedicalDevice"]
        references = [
            x.strip()
            for x in self._state_split(self.read_cell_by_name(index, "appliesTo"))
        ]
        for reference in references:
            if reference:
                found = False
                for klass in klasses:
                    xref = self.globals.cross_references.get(klass, reference)
                    if xref:
                        results.append(xref.id)
                        found = True
                        break
                if not found:
                    self._error(
                        index,
                        self._get_column_index("appliesTo"),
                        f"Could not resolve appliesTo reference '{reference}'",
                    )
        return results
