from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm.study_design_population import StudyDesignPopulation
from usdm.code import Code
from usdm_excel.cdisc_ct_library import cdisc_ct_library
from usdm_excel.cdisc_ct import CDISCCT

class StudyDesignPopulationSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignPopulations'))
      self.populations = []
      for index, row in self.sheet.iterrows():
        description = self.clean_cell(row, index, "populationDescription")
        number = self.clean_cell(row, index, "plannedNumberOfParticipants")
        min = self.clean_cell(row, index, "plannedMinimumAgeOfParticipants")
        max = self.clean_cell(row, index, "plannedMaximumAgeOfParticipants")
        codes = self._build_codes(row, index)
        #print("POP:", description, number, min, max, codes)
        self.populations.append(
          StudyDesignPopulation(studyDesignPopulationId=id_manager.build_id(StudyDesignPopulation), 
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
    ct = cdisc_ct_library.klass_and_attribute('StudyDesignPopulation', 'plannedSexOfParticipants', value)
    if not ct == None:
      result.append(CDISCCT().code(code=ct['conceptId'], decode=ct['preferredTerm']))
    return result