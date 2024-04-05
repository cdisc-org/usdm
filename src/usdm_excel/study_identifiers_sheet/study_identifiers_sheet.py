import traceback
from usdm_model.organization import Organization
from usdm_model.study_identifier import StudyIdentifier
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.managers import Managers


class StudyIdentifiersSheet(BaseSheet):

  SHEET_NAME = 'studyIdentifiers'
  
  def __init__(self, file_path, managers: Managers):
    try:
      super().__init__(file_path=file_path, managers=managers, sheet_name=self.SHEET_NAME)
      self.identifiers = []
      self.process_sheet()
    except Exception as e:
      self._general_sheet_exception(e)
      
  def process_sheet(self):
    self.identifiers = []
    for index, row in self.sheet.iterrows():
      org_type = self.read_cdisc_klass_attribute_cell_by_name('Organization', 'organizationType', index, ['organisationType', 'type'])     
      org_id_scheme = self.read_cell_by_name(index, 'organisationIdentifierScheme')
      org_identifier = self.read_cell_by_name(index, 'organisationIdentifier')
      org_name = self.read_cell_by_name(index, ['organisationName', 'name'])
      org_label = self.read_cell_by_name(index, 'label', default="", must_be_present=False)
      org_address = self.read_address_cell_by_name(index, 'organisationAddress')
      if org_address:
        self.managers.cross_references.add(org_address.id, org_address)   
      try:
        organisation = Organization(
          id=self.managers.id_manager.build_id(Organization),
          identifierScheme=org_id_scheme, 
          identifier=org_identifier,
          name=org_name,
          label=org_label,
          organizationType=org_type,
          legalAddress=org_address
        )
      except Exception as e:
        self._general_error(f"Failed to create Organization object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")
      else:
        self.managers.cross_references.add(organisation.id, organisation)   
        try:
          item = StudyIdentifier(
            id=self.managers.id_manager.build_id(StudyIdentifier),
            studyIdentifier=self.read_cell_by_name(index, 'studyIdentifier'), 
            studyIdentifierScope=organisation
          )
        except Exception as e:
          self._general_error(f"Failed to create StudyIdentifier object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          self.identifiers.append(item)
          self.managers.cross_references.add(item.studyIdentifier, item)         
