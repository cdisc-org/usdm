from usdm_model.organization import Organization
from usdm_model.address import Address
from usdm_model.study_identifier import StudyIdentifier
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.iso_3166 import ISO3166
from usdm_excel.cross_ref import cross_references
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
      org_type = self.read_cdisc_klass_attribute_cell_by_name('Organization', 'organizationType', index, ['organisationType', 'type'])     
      org_id_scheme = self.read_cell_by_name(index, 'organisationIdentifierScheme')
      org_identifier = self.read_cell_by_name(index, 'organisationIdentifier')
      org_name = self.read_cell_by_name(index, ['organisationName', 'name'])
      org_label = self.read_cell_by_name(index, 'label', default="")
      org_address = self._build_address(index)
      try:
        organisation = Organization(
          id=id_manager.build_id(Organization),
          organizationIdentifierScheme=org_id_scheme, 
          organizationIdentifier=org_identifier,
          name=org_name,
          label=org_label,
          type=org_type,
          organizationLegalAddress=org_address
        )
      except Exception as e:
        self._general_error(f"Failed to create Organization object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")
      else:
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
  def _build_address(self, row_index):
    field_name = 'organisationAddress'
    raw_address = self.read_cell_by_name(row_index, field_name)
    # TODO The '|' separator is preserved for legacy reasons but should be removed in the future
    if '|' in raw_address:
      sep = '|'
      parts = raw_address.split(sep)
    else:
      sep = ','
      parts = self._state_split(raw_address)
    if len(parts) == 6:
      # TODO Put something in each part if empty. Temp fix
      for index, part in enumerate(parts):
        parts[index] = '-' if part == '' else part.strip()
      result = self._to_address(
          id_manager.build_id(Address),
          parts[0], 
          parts[1], 
          parts[2], 
          parts[3], 
          parts[4], 
          ISO3166().code(parts[5])
        )
      return result
    else:
      col_index = self.sheet.columns.get_loc(field_name)
      self._error(row_index, col_index, f"Address does not contain the required fields (line, city, district, state, postal code and country code) using '{sep}' separator characters, only {len(parts)} found")
      return None

  def _to_address(self, id, line, city, district, state, postal_code, country):
    text = "%s, %s, %s, %s, %s, %s" % (line, city, district, state, postal_code, country.decode)
    text = text.replace(' ,', '')
    try:
      result = Address(id=id, text=text, line=line, city=city, district=district, state=state, postalCode=postal_code, country=country)
    except Exception as e:
      self._general_error(f"Failed to create Address object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      result = None
    return result