from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_identifiers_sheet.study_identifiers_sheet import StudyIdentifiersSheet
from usdm_excel.study_design_sheet.study_design_sheet import StudyDesignSheet
from usdm_excel.study_soa_sheet.study_soa_sheet import StudySoASheet
from usdm_excel.alias import Alias
from usdm.study import Study
import traceback
import pandas as pd

class StudySheet(BaseSheet):

  def __init__(self, file_path, id_manager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='study'), id_manager)
      self.study = None
      self.study_identifiers = StudyIdentifiersSheet(file_path, id_manager)
      self.study_design = StudyDesignSheet(file_path, id_manager)
      self.soa = StudySoASheet(file_path, id_manager)
      
      study_design = self.study_design.study_designs[0]
      study_design.studyScheduleTimelines.append(self.soa.timelines[0])
      study_design.encounters = self.soa.encounters
            
      self.process_sheet()
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()

  def process_sheet(self):
    for index, row in self.sheet.iterrows():
      study_phase = Alias(self.id_manager).code(self.cdisc_code_cell(self.clean_cell(row, index, "studyPhase")), [])
      study_version = self.clean_cell(row, index, "studyVersion")
      study_type = self.cdisc_code_cell(self.clean_cell(row, index, "studyType"))
      study_title = self.clean_cell(row, index, "studyTitle")
      self.study = Study(
        studyId=None, # No Id, will be allocated a UUID
        studyTitle=study_title,
        studyVersion=study_version,
        studyType=study_type,
        studyPhase=study_phase,
        businessTherapeuticAreas=[],
        studyRationale="",
        studyAcronym="",
        studyIdentifiers=self.study_identifiers.identifiers,
        studyProtocolVersions=[],
        studyDesigns=self.study_design.study_designs
      )

  def study_sponsor(self):
    return self.cdisc_code(code="C93453", decode="Study Registry")

  def study_regulatory(self):
    return self.cdisc_code(code="C93453", decode="Study Registry")

  def the_study(self):
    return self.study