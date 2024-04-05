import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.organization import ResearchOrganization
from usdm_model.study_site import StudySite
from usdm_excel.utility import general_sheet_exception
from usdm_excel.managers import Managers

class StudyDesignSitesSheet(BaseSheet):

  SHEET_NAME = 'studyDesignSites'
  
  def __init__(self, file_path: str, managers: Managers):
    try:
      self.organizations = []
      self.sites = []
      super().__init__(file_path=file_path, managers=managers, sheet_name=self.SHEET_NAME, optional=True)
      if self.success:
        current_org = None
        for index, row in self.sheet.iterrows():
          org_name = self.read_cell_by_name(index, 'name')
          site_name = self.read_cell_by_name(index, 'siteName')
          site_description = self.read_cell_by_name(index, 'siteDescription')
          site_label = self.read_cell_by_name(index, 'siteLabel')
          site = self.create_object(StudySite, {'name': site_name, 'description': site_description, 'label': site_label})
          if site:
            self.sites.append(site)
            self.managers.cross_references.add(site.id, site)     
          if org_name:
            org_label = self.read_cell_by_name(index, 'label')
            org_type = self.read_cdisc_klass_attribute_cell_by_name('Organization', 'organizationType', index, ['type'])     
            org_id_scheme = self.read_cell_by_name(index, 'identifierScheme')
            org_identifier = self.read_cell_by_name(index, 'identifier')
            org_address = self.read_address_cell_by_name(index, 'address')
            if org_address:
              self.managers.cross_references.add(org_address.id, org_address)   
            item = self.create_object(ResearchOrganization, {'identifierScheme': org_id_scheme, 'identifier': org_identifier, 'name': org_name, 'label': org_label, 'organizationType': org_type, 'legalAddress': org_address, 'manages': [site]})
            if item:
              self.organizations.append(item)
              self.managers.cross_references.add(item.id, item)     
              current_org = item
          else:
            current_org.manages.append(site)
    except Exception as e:
      general_sheet_exception(self.SHEET_NAME, e)

