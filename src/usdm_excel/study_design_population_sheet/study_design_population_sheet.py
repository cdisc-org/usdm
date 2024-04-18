from usdm_excel.base_sheet import BaseSheet
from usdm_model.population_definition import StudyDesignPopulation, StudyCohort
from usdm_model.range import Range
from usdm_model.characteristic import Characteristic
from usdm_excel.globals import Globals

class StudyDesignPopulationSheet(BaseSheet):

  SHEET_NAME = 'studyDesignPopulations'
  
  def __init__(self, file_path: str, globals: Globals):
    try:
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME)
      self.population = None
      self._cohorts = []
      for index, row in self.sheet.iterrows():
        level = self.read_cell_by_name(index, 'level')
        name = self.read_cell_by_name(index, 'name')
        description = self.read_cell_by_name(index, 'description')
        label = self.read_cell_by_name(index, 'label')
        required_number = self.read_range_cell_by_name(index, "plannedCompletionNumber", require_units=False, allow_empty=True)
        recruit_number = self.read_range_cell_by_name(index, "plannedEnrollmentNumber", require_units=False, allow_empty=True)
        planned_age = self.read_range_cell_by_name(index, "plannedAge", require_units=True, allow_empty=True)
        healthy = self.read_boolean_cell_by_name(index, 'includesHealthySubjects', must_be_present=False)
        characteristics = self.read_cell_multiple_by_name(index, 'characteristics', must_be_present=False)
        codes = self._build_codes(row, index)
        if level.upper() == "MAIN":
          self.population = self._study_population(name, description, label, recruit_number, required_number, planned_age, healthy, codes)
        else:
          cohort = self._study_cohort(name, description, label, recruit_number, required_number, planned_age, healthy, codes, characteristics)
      if self.population: 
        self.population.cohorts = self._cohorts
      else:
        self._general_error(f"Not main study population detected")
    except Exception as e:
      self._sheet_exception(e)

  def _build_codes(self, row, index):
    code = self.read_cdisc_klass_attribute_cell_by_name('StudyDesignPopulation', "plannedSexOfParticipants", index, "plannedSexOfParticipants", allow_empty=True)
    return [code] if code else []

  def _study_population(self, name: str, description: str, label: str, recruit_number: Range, required_number: Range, planned_age: Range, healthy: bool, codes: list) -> StudyDesignPopulation:    
    params = {
      'name': name,
      'description': description,
      'label': label,
      'includesHealthySubjects': healthy,
      'plannedEnrollmentNumber': recruit_number,
      'plannedCompletionNumber': required_number,
      'plannedAge': planned_age,
      'plannedSex': codes
    }
    item = self.create_object(StudyDesignPopulation, params)
    if item:
      self.globals.cross_references.add(name, item)
    return item

  def _study_cohort(self, name: str, description: str, label: str, recruit_number: Range, required_number: Range, planned_age: Range, healthy: bool, codes: list, characteristics: list) -> StudyCohort:    
    characteristic_refs = self._resolve_characteristics(characteristics)
    params = {  
      'name': name,
      'description': description,
      'label': label,
      'includesHealthySubjects': healthy,
      'plannedEnrollmentNumber': recruit_number,
      'plannedCompletionNumber': required_number,
      'plannedAge': planned_age,
      'plannedSex': codes,
      'characteristics': characteristic_refs
    }
    item = self.create_object(StudyCohort, params)
    if item:
      self.globals.cross_references.add(name, item)
      self._cohorts.append(item)
    return item
      
  def _resolve_characteristics(self, names):
    results = []
    for name in names:
      object = self.globals.cross_references.get(Characteristic, name)
      if object:
        results.append(object)
      else:
        self._general_warning(f"Characterisitc '{name}' not found")
    return results
