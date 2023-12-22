from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.organization import ResearchOrganization
from usdm_model.study_site import StudySite

class StudyDesignSitesSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      self.organizations = []
      self.sites = []
      super().__init__(file_path=file_path, sheet_name='studyDesignSites', optional=True)
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
            cross_references.add(site.id, site)     
          if org_name:
            org_label = self.read_cell_by_name(index, 'label')
            org_type = self.read_cdisc_klass_attribute_cell_by_name('Organization', 'organizationType', index, ['type'])     
            org_id_scheme = self.read_cell_by_name(index, 'identifierScheme')
            org_identifier = self.read_cell_by_name(index, 'identifier')
            org_address = self.read_address_cell_by_name(index, 'address')
            if org_address:
              cross_references.add(org_address.id, org_address)   
            item = self.create_object(ResearchOrganization, {'identifierScheme': org_id_scheme, 'identifier': org_identifier, 'name': org_name, 'label': org_label, 'type': org_type, 'legalAddress': org_address, 'manageIds': [site.id]})
            if item:
              self.organizations.append(item)
              cross_references.add(item.id, item)     
              current_org = item
          else:
            current_org.manageIds.append(site.id)
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

