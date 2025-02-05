from usdm_excel.base_sheet import BaseSheet
from usdm_excel.iso_3166 import ISO3166
from usdm_model.study_site import StudySite
from usdm_model.organization import Organization
from usdm_excel.globals import Globals


class StudyDesignSitesSheet(BaseSheet):
    SHEET_NAME = "studyDesignSites"

    def __init__(self, file_path: str, globals: Globals):
        try:
            self.items: list[StudySite] = []
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=self.SHEET_NAME,
                optional=True,
            )
            if self.success:
                for index, row in self.sheet.iterrows():
                    org_name = self.read_cell_by_name(index, ["organization"])
                    site_name = self.read_cell_by_name(index, ["siteName", "name"])
                    site_description = self.read_cell_by_name(
                        index, ["siteDescription", "description"]
                    )
                    site_label = self.read_cell_by_name(index, ["siteLabel", "label"])
                    site_country = ISO3166(self.globals).code(
                        self.read_cell_by_name(index, ["siteCountry", "country"])
                    )
                    site = self.create_object(
                        StudySite,
                        {
                            "name": site_name,
                            "description": site_description,
                            "label": site_label,
                            "country": site_country,
                        },
                    )
                    if site:
                        self.items.append(site)
                        self.globals.cross_references.add(site.name, site)
                        if org_name:
                            org: Organization = self.globals.cross_references.get(
                                Organization, org_name
                            )
                            if org:
                                org.managedSites.append(site)
                            else:
                                self._error(
                                    index,
                                    "organization",
                                    f"Failed to find organization with name '{org_name}'",
                                )
                        else:
                            self._error(
                                index,
                                "organization",
                                f"No organization specified for site '{site_name}'",
                            )
        except Exception as e:
            self._sheet_exception(e)
