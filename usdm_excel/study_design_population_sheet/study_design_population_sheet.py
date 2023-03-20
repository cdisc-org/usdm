from usdm_excel.base_sheet import BaseSheet
import traceback
import pandas as pd
from usdm.study_design_population import StudyDesignPopulation
from usdm_excel.cdisc_ct_library import cdisc_ct_library

class StudyDesignPopulationSheet(BaseSheet):

  def __init__(self, file_path, id_manager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignPopulation'), id_manager)
      self.populations = []
      for index, row in self.sheet.iterrows():
        description = self.clean_cell(row, index, "populationDescription")
        number = self.clean_cell(row, index, "plannedNumberOfParticipants")
        min = self.clean_cell(row, index, "plannedMinimumAgeOfParticipants")
        max = self.clean_cell(row, index, "plannedMaximumAgeOfParticipants")
        codes = self._build_codes(row, index)
        print("POP:", description, number, min, max, codes)
        self.populations.append(
          StudyDesignPopulation(studyDesignPopulationId=self.id_manager.build_id(StudyDesignPopulation), 
            populationDescription=description, 
            plannedNumberOfParticipants=number,
            plannedMinimumAgeOfParticipants=min,
            plannedMaximumAgeOfParticipants=max,
            codes=codes
          )
        )
        
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()

  def _build_codes(self, row, index):
    result = []
    value = self.clean_cell(row, index, "plannedSexOfParticipants")
    code = cdisc_ct_library.klass_and_attribute('StudyDesignPopulation', 'plannedSexOfParticipants', value)
    if not code == None:
      result.append(code)
    return result