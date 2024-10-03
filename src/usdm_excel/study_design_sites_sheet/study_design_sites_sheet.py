from usdm_excel.base_sheet import BaseSheet
from usdm_model.study_site import StudySite
from usdm_model.organization import Organization
from usdm_excel.globals import Globals

class StudyDesignSitesSheet(BaseSheet):

  SHEET_NAME = 'studyDesignSites'
  
  def __init__(self, file_path: str, globals: Globals):
    try:
      self.organizations: list[Organization] = []
      self.sites: list[StudySite] = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME, optional=True)
      if self.success:
        current_org: Organization = None
        for index, row in self.sheet.iterrows():
          org_name = self.read_cell_by_name(index, 'name')
          site_name = self.read_cell_by_name(index, 'siteName')
          site_description = self.read_cell_by_name(index, 'siteDescription')
          site_label = self.read_cell_by_name(index, 'siteLabel')
          site = self.create_object(StudySite, {'name': site_name, 'description': site_description, 'label': site_label})
          if site:
            self.sites.append(site)
            self.globals.cross_references.add(site.name, site)     
          if org_name:
            org_label = self.read_cell_by_name(index, 'label')
            org_type = self.read_cdisc_klass_attribute_cell_by_name('Organization', 'organizationType', index, ['type'])     
            org_id_scheme = self.read_cell_by_name(index, 'identifierScheme')
            org_identifier = self.read_cell_by_name(index, 'identifier')
            org_address = self.read_address_cell_by_name(index, 'address')
            if org_address:
              self.globals.cross_references.add(org_address.id, org_address)   
            item = self.create_object(Organization, {'identifierScheme': org_id_scheme, 'identifier': org_identifier, 'name': org_name, 'label': org_label, 'type': org_type, 'legalAddress': org_address, 'managedSites': [site]})
            if item:
              self.organizations.append(item)
              self.globals.cross_references.add(item.id, item)     
              current_org = item
          else:
            current_org.managedSites.append(site)
    except Exception as e:
      self._sheet_exception(e)

