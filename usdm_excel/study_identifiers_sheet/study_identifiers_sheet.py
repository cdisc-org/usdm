from model.organisation import Organisation
from model.address import Address
from model.study_identifier import StudyIdentifier
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import IdManager
from usdm_excel.cdisc import CDISC
from usdm_excel.iso_3166 import ISO3166
import pandas as pd
import traceback

class StudyIdentifiersSheet(BaseSheet):

  def __init__(self, file_path: str, id_manager: IdManager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyIdentifiers'), id_manager)
      self.identifiers = []
      self.id_manager = id_manager
      self.process_sheet()
    except Exception as e:
      print("Oops! (Study Identifiers Sheet)", e, "occurred.")
      traceback.print_exc()
      
  def process_sheet(self):
    self.identifiers = []
    for index, row in self.sheet.iterrows():
      organisation_type_key = self.clean_cell(row, index, 'organisationType')
      if organisation_type_key.lower() == "sponsor":
        organisation_type = self.study_sponsor()
      elif organisation_type_key.lower() == "registry":
        organisation_type = self.study_registry()
      elif organisation_type_key.lower() == "regulatory":
        organisation_type = self.regulatory()
      else:
        organisation_type = self.study_sponsor()
      organisation = Organisation(
        organizationId=self.id_manager.build_id(Organisation),
        scheme=self.clean_cell(row, index, 'organisationIdentifierScheme'), 
        identifier=self.clean_cell(row, index, 'organisationIdentifier'),
        name=self.clean_cell(row, index, 'organisationName'),
        type=organisation_type,
        address=Address.add_address("Unknown Lane", "Somewhere", "Back of Beyond", "City of the Lost", "12345", ISO3166.code("USA", "United States of America"))
      )
      self.identifiers.append(StudyIdentifier(
        self.id_manager.build_id(StudyIdentifier),
        identifier=self.clean_cell(row, index, 'studyIdentifier'), 
        scope=organisation)
      )
    
  def study_registry(self):
    return CDISC.code(code="C93453", decode="Study Registry")

  def study_sponsor(self):
    return CDISC.code(code="C70793", decode="Clinical Study Sponsor")

  def regulatory(self):
    return CDISC.code(code="C188863", decode="Regulatory Agency")
