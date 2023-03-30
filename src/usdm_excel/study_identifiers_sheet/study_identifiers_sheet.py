from usdm.organisation import Organisation
from usdm.address import Address
from usdm.study_identifier import StudyIdentifier
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.iso_3166 import ISO3166
import pandas as pd
import traceback

class StudyIdentifiersSheet(BaseSheet):

  def __init__(self, file_path: str):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyIdentifiers'))
      self.identifiers = []
      self.process_sheet()
    except Exception as e:
      print("Oops! (Study Identifiers Sheet)", e, "occurred.")
      traceback.print_exc()
      
  def process_sheet(self):
    self.identifiers = []
    for index, row in self.sheet.iterrows():
      organisation_type = self.cdisc_klass_attribute_cell('Organisation', 'organisationType', self.clean_cell(row, index, 'organisationType'))
      raw_address=self.clean_cell(row, index, 'organisationAddress')
      organisation = Organisation(
        organisationId=id_manager.build_id(Organisation),
        organisationIdentifierScheme=self.clean_cell(row, index, 'organisationIdentifierScheme'), 
        organisationIdentifier=self.clean_cell(row, index, 'organisationIdentifier'),
        organisationName=self.clean_cell(row, index, 'organisationName'),
        organisationType=organisation_type,
        organizationLegalAddress=self._build_address(raw_address)
      )
      self.identifiers.append(StudyIdentifier(
        studyIdentifierId=id_manager.build_id(StudyIdentifier),
        studyIdentifier=self.clean_cell(row, index, 'studyIdentifier'), 
        studyIdentifierScope=organisation)
      )
    
  def _build_address(self, raw_address):
    parts = raw_address.split("|")
    if len(parts) == 6:
      return Address.add_address(
            id_manager.build_id(Address),
            parts[0].strip(), 
            parts[1].strip(), 
            parts[2].strip(), 
            parts[3].strip(), 
            parts[4].strip(), 
            ISO3166().code(parts[5].strip())
          )
    else:
      return None