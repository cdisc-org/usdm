import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.population_definition import StudyDesignPopulation, StudyCohort
from usdm_excel.managers import Managers
from usdm_excel.utility import general_sheet_exception

class StudyDesignPopulationSheet(BaseSheet):

  SHEET_NAME = 'studyDesignPopulations'
  
  def __init__(self, file_path: str, managers: Managers):
    try:
      super().__init__(file_path=file_path, managers=managers, sheet_name=self.SHEET_NAME)
      self.population = None
      cohorts = []
      for index, row in self.sheet.iterrows():
        level = self.read_cell_by_name(index, 'level')
        name = self.read_cell_by_name(index, 'name')
        description = self.read_cell_by_name(index, 'description')
        label = self.read_cell_by_name(index, 'label')
        required_number = self.read_range_cell_by_name(index, "plannedCompletionNumber", require_units=False, allow_empty=True)
        recruit_number = self.read_range_cell_by_name(index, "plannedEnrollmentNumber", require_units=False, allow_empty=True)
        planned_age = self.read_range_cell_by_name(index, "plannedAge", require_units=True, allow_empty=True)
        healthy = self.read_boolean_cell_by_name(index, 'includesHealthySubjects', must_be_present=False)
        codes = self._build_codes(row, index)
        if level.upper() == "MAIN":
          self.population = self._study_population(name, description, label, recruit_number, required_number, planned_age, healthy, codes)
        else:
          cohort = self._study_cohort(name, description, label, recruit_number, required_number, planned_age, healthy, codes)
          cohorts.append(cohort)
      if self.population: 
        self.population.cohorts = cohorts
      else:
        self._general_error(f"Not main study population detected")
    except Exception as e:
      general_sheet_exception(self.SHEET_NAME, e)

  def _build_codes(self, row, index):
    code = self.read_cdisc_klass_attribute_cell_by_name('StudyDesignPopulation', "plannedSexOfParticipants", index, "plannedSexOfParticipants", allow_empty=True)
    return [code] if code else []

  def _study_population(self, name, description, label, recruit_number, required_number, planned_age, healthy, codes):    
    try:
      item = StudyDesignPopulation(id=self.managers.id_manager.build_id(StudyDesignPopulation),
        name=name,
        description=description,
        label=label,
        includesHealthySubjects=healthy,
        plannedEnrollmentNumber=recruit_number,
        plannedCompletionNumber=required_number,
        plannedAge=planned_age,
        plannedSex=codes
      )
    except Exception as e:
      self._general_error(f"Failed to create StudyDesignPopulation object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      return None
    else:
      self.managers.cross_references.add(name, item)
      return item

  def _study_cohort(self, name, description, label, recruit_number, required_number, planned_age, healthy, codes):    
    try:
      item = StudyCohort(id=self.managers.id_manager.build_id(StudyCohort),
        name=name,
        description=description,
        label=label,
        includesHealthySubjects=healthy,
        plannedEnrollmentNumber=recruit_number,
        plannedCompletionNumber=required_number,
        plannedAge=planned_age,
        plannedSex=codes,
        characteristics=[]
      )
    except Exception as e:
      self._general_error(f"Failed to create StudyCohort object, exception {e}")
      #print(f"{traceback.format_exc()}")
      self._traceback(f"{traceback.format_exc()}")
      return None
    else:
      self.managers.cross_references.add(name, item)
      return item