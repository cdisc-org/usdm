from usdm_model.identifier import StudyIdentifier
from usdm_model.organization import Organization
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.globals import Globals


class StudyOrganizationsSheet(BaseSheet):
    SHEET_NAME = "studyOrganizations"

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
            org_type = self.read_cdisc_klass_attribute_cell_by_name(
                "Organization",
                "organizationType",
                index,
                ["organisationType", "organizationType", "type"],
            )
            org_id_scheme = self.read_cell_by_name(
                index,
                [
                    "organisationIdentifierScheme",
                    "organizationIdentifierScheme",
                    "identifierScheme",
                ],
            )
            org_identifier = self.read_cell_by_name(
                index,
                ["organisationIdentifier", "organizationIdentifier", "identifier"],
            )
            org_name = self.read_cell_by_name(
                index, ["organisationName", "organizationName", "name"]
            )
            org_label = self.read_cell_by_name(
                index, "label", default="", must_be_present=False
            )
            org_address = self.read_address_cell_by_name(
                index, ["organisationAddress", "organizationAddress", "address"]
            )
            if org_address:
                self.globals.cross_references.add(org_address.id, org_address)
            organization: Organization = self.create_object(
                Organization,
                {
                    "identifierScheme": org_id_scheme,
                    "identifier": org_identifier,
                    "name": org_name,
                    "label": org_label,
                    "type": org_type,
                    "legalAddress": org_address,
                },
            )
            if organization:
                self.globals.cross_references.add(organization.name, organization)
                self.items.append(organization)
