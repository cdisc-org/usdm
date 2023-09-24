from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.study_design_population import StudyDesignPopulation

class StudyDesignPopulationSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignPopulations')
      self.populations = []
      for index, row in self.sheet.iterrows():
        name = self.read_cell_by_name(index, 'name', default=f"POP {index + 1}") # 'name' added, preserve backward compatibility so defaulted
        description = self.read_description_by_name(index, ['description', 'populationDescription']) # Allow multiple names for column
        label = self.read_cell_by_name(index, 'label', default="")
        number = self.read_cell_by_name(index, "plannedNumberOfParticipants")
        min = self.read_cell_by_name(index, "plannedMinimumAgeOfParticipants")
        max = self.read_cell_by_name(index, "plannedMaximumAgeOfParticipants")
        codes = self._build_codes(row, index)
        try:
          pop = StudyDesignPopulation(id=id_manager.build_id(StudyDesignPopulation),
            name=name,
            description=description,
            label=label,
            plannedNumberOfParticipants=number,
            plannedMinimumAgeOfParticipants=min,
            plannedMaximumAgeOfParticipants=max,
            plannedSexOfParticipants=codes
          )
        except Exception as e:
          self._general_error(f"Failed to create StudyDesignPopulation object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          self.populations.append(pop)
        
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      #print(f"{traceback.format_exc()}")
      self._traceback(f"{traceback.format_exc()}")

  def _build_codes(self, row, index):
    code = self.read_cdisc_klass_attribute_cell_by_name('StudyDesignPopulation', "plannedSexOfParticipants", index, "plannedSexOfParticipants")
    return [code] if code else []
      

        