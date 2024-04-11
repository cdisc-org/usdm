import traceback
from usdm_model.organization import Organization
from usdm_model.study_identifier import StudyIdentifier
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.globals import Globals


class StudyIdentifiersSheet(BaseSheet):

  SHEET_NAME = 'studyIdentifiers'
  
  def __init__(self, file_path, globals: Globals):
    try:
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME)
      self.identifiers = []
      self.process_sheet()
    except Exception as e:
      self._sheet_exception(e)
      
  def process_sheet(self):
    self.identifiers = []
    for index, row in self.sheet.iterrows():
      org_type = self.read_cdisc_klass_attribute_cell_by_name('Organization', 'organizationType', index, ['organisationType', 'organizationType', 'type'])     
      org_id_scheme = self.read_cell_by_name(index, ['organisationIdentifierScheme', 'organizationIdentifierScheme', 'identifierScheme'])
      org_identifier = self.read_cell_by_name(index, ['organisationIdentifier', 'organizationIdentifier'])
      org_name = self.read_cell_by_name(index, ['organisationName', 'organizationName', 'name'])
      org_label = self.read_cell_by_name(index, 'label', default="", must_be_present=False)
      org_address = self.read_address_cell_by_name(index, ['organisationAddress', 'organizationAddress', 'address'])
      if org_address:
        self.globals.cross_references.add(org_address.id, org_address)   
      try:
        organisation = Organization(
          id=self.globals.id_manager.build_id(Organization),
          identifierScheme=org_id_scheme, 
          identifier=org_identifier,
          name=org_name,
          label=org_label,
          organizationType=org_type,
          legalAddress=org_address
        )
      except Exception as e:
        self._general_exception(f"Failed to create Organization object", e)
      else:
        self.globals.cross_references.add(organisation.id, organisation)   
        try:
          item = StudyIdentifier(
            id=self.globals.id_manager.build_id(StudyIdentifier),
            studyIdentifier=self.read_cell_by_name(index, 'studyIdentifier'), 
            studyIdentifierScope=organisation
          )
        except Exception as e:
          self._general_exception(f"Failed to create StudyIdentifier object", e)
        else:
          self.identifiers.append(item)
          self.globals.cross_references.add(item.studyIdentifier, item)         
