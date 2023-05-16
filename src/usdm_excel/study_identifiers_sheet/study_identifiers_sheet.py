from usdm_model.organisation import Organisation
from usdm_model.address import Address
from usdm_model.study_identifier import StudyIdentifier
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.iso_3166 import ISO3166
import pandas as pd
import traceback

class StudyIdentifiersSheet(BaseSheet):

  def __init__(self, file_path: str):
    try:
      super().__init__(file_path=file_path, sheet_name='studyIdentifiers')
      self.identifiers = []
      self.process_sheet()
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")
      
  def process_sheet(self):
    self.identifiers = []
    for index, row in self.sheet.iterrows():
      organisation_type = self.read_cdisc_klass_attribute_cell_by_name('Organisation', 'organisationType', index, 'organisationType')     
      organisation = Organisation(
        organisationId=id_manager.build_id(Organisation),
        organisationIdentifierScheme=self.read_cell_by_name(index, 'organisationIdentifierScheme'), 
        organisationIdentifier=self.read_cell_by_name(index, 'organisationIdentifier'),
        organisationName=self.read_cell_by_name(index, 'organisationName'),
        organisationType=organisation_type,
        organizationLegalAddress=self._build_address(index)
      )
      self.identifiers.append(StudyIdentifier(
        studyIdentifierId=id_manager.build_id(StudyIdentifier),
        studyIdentifier=self.read_cell_by_name(index, 'studyIdentifier'), 
        studyIdentifierScope=organisation)
      )
    
  def _build_address(self, row_index):
    field_name = 'organisationAddress'
    raw_address = self.read_cell_by_name(row_index, field_name)
    # The '|' separator is preserved for legacy reasons but should be removed in the future
    if '|' in raw_address:
      sep = '|'
      parts = raw_address.split(sep)
    else:
      sep = ','
      parts = self._state_split(raw_address)
    if len(parts) == 6:
      result = self._to_address(
          id_manager.build_id(Address),
          parts[0].strip(), 
          parts[1].strip(), 
          parts[2].strip(), 
          parts[3].strip(), 
          parts[4].strip(), 
          ISO3166().code(parts[5].strip())
        )
      return result
    else:
      col_index = self.sheet.columns.get_loc(field_name)
      self._error(row_index, col_index, f"Address does not contain the required fields (line, city, district, state, postal code and country code) using '{sep}' separator characters, only {len(parts)} found")
      return None

  def _to_address(self, id, line, city, district, state, postal_code, country):
    text = "%s, %s, %s, %s, %s, %s" % (line, city, district, state, postal_code, country.decode)
    text = text.replace(' ,', '')
    result = Address(addressId=id, text=text, line=line, city=city, district=district, state=state, postalCode=postal_code, country=country)
    return result