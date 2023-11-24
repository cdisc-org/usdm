from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
import traceback
from usdm_model.study_design_population import StudyDesignPopulation
from usdm_model.study_cohort import StudyCohort

class StudyDesignPopulationSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignPopulations')
      self.population = None
      cohorts = []
      for index, row in self.sheet.iterrows():
        level = self.read_cell_by_name(index, 'level')
        name = self.read_cell_by_name(index, 'name')
        description = self.read_description_by_name(index, 'description')
        label = self.read_cell_by_name(index, 'label')
        required_number = self.read_range_cell_by_name(index, "plannedCompletionNumber", require_units=False, allow_empty=True)
        recruit_number = self.read_range_cell_by_name(index, "plannedEnrollmentNumber", require_units=False, allow_empty=True)
        min = self.read_quantity_cell_by_name(index, "plannedMinimumAge", allow_empty=True)
        max = self.read_quantity_cell_by_name(index, "plannedMaximumAge", allow_empty=True)
        codes = self._build_codes(row, index)
        if level.upper() == "MAIN":
          self.population = self._study_population(name, description, label, recruit_number, required_number, min, max, codes)
        else:
          cohort = self._study_cohort(name, description, label, recruit_number, required_number, min, max, codes)
          cohorts.append(cohort)
      if self.population: 
        self.population.cohorts = cohorts
      else:
        self._general_error(f"Not main study population detected")
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet")
      print(f"{traceback.format_exc()}")
      self._traceback(f"{traceback.format_exc()}")

  def _build_codes(self, row, index):
    code = self.read_cdisc_klass_attribute_cell_by_name('StudyDesignPopulation', "plannedSexOfParticipants", index, "plannedSexOfParticipants", allow_empty=True)
    return [code] if code else []

  def _study_population(self, name, description, label, recruit_number, required_number, min, max, codes):    
    try:
      item = StudyDesignPopulation(id=id_manager.build_id(StudyDesignPopulation),
        name=name,
        description=description,
        label=label,
        plannedEnrollmentNumber=recruit_number,
        plannedCompletionNumber=required_number,
        plannedMinimumAgeOfParticipants=min,
        plannedMaximumAgeOfParticipants=max,
        plannedSexOfParticipants=codes
      )
    except Exception as e:
      self._general_error(f"Failed to create StudyDesignPopulation object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      return None
    else:
      cross_references.add(name, item)
      return item

  def _study_cohort(self, name, description, label, recruit_number, required_number, min, max, codes):    
    try:
      item = StudyCohort(id=id_manager.build_id(StudyCohort),
        name=name,
        description=description,
        label=label,
        plannedEnrollmentNumber=recruit_number,
        plannedCompletionNumber=required_number,
        plannedMinimumAgeOfParticipants=min,
        plannedMaximumAgeOfParticipants=max,
        plannedSexOfParticipants=codes,
        characteristics=[]
      )
    except Exception as e:
      self._general_error(f"Failed to create StudyCohort object, exception {e}")
      print(f"{traceback.format_exc()}")
      self._traceback(f"{traceback.format_exc()}")
      return None
    else:
      cross_references.add(name, item)
      return item