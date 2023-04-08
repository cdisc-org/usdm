from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.study_design_population import StudyDesignPopulation

class StudyDesignPopulationSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      #super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignPopulations'))
      super().__init__(file_path=file_path,  sheet_name='studyDesignPopulations')
      self.populations = []
      for index, row in self.sheet.iterrows():
        description = self.read_cell_by_name(index, "populationDescription")
        number = self.read_cell_by_name(index, "plannedNumberOfParticipants")
        min = self.read_cell_by_name(index, "plannedMinimumAgeOfParticipants")
        max = self.read_cell_by_name(index, "plannedMaximumAgeOfParticipants")
        codes = self._build_codes(row, index)
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
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")


  def _build_codes(self, row, index):
    #result = []
    return [self.read_cdisc_klass_attribute_cell_by_name('StudyDesignPopulation', "plannedSexOfParticipants", index, "plannedSexOfParticipants")]
