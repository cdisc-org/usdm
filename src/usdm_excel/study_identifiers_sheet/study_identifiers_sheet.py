from usdm_model.organization import Organization
from usdm_model.study_identifier import StudyIdentifier
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
import traceback

class StudyIdentifiersSheet(BaseSheet):

  def __init__(self, file_path: str):
    try:
      super().__init__(file_path=file_path, sheet_name='studyIdentifiers')
      self.identifiers = []
      self.process_sheet()
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")
      
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
        cross_references.add(org_address.id, org_address)   
      try:
        organisation = Organization(
          id=id_manager.build_id(Organization),
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
        cross_references.add(organisation.id, organisation)   
        try:
          item = StudyIdentifier(
            id=id_manager.build_id(StudyIdentifier),
            studyIdentifier=self.read_cell_by_name(index, 'studyIdentifier'), 
            studyIdentifierScope=organisation
          )
        except Exception as e:
          self._general_error(f"Failed to create StudyIdentifier object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          self.identifiers.append(item)
          cross_references.add(item.studyIdentifier, item)         
