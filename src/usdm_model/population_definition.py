from typing import Union, List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .range import Range
from .eligibility_criteria import EligibilityCriteria
from .characteristic import Characteristic

class PopulationDefinition(ApiBaseModelWithIdNameLabelAndDesc):
  includesHealthySubjects: bool
  plannedEnrollmentNumber: Union[Range, None] = None
  plannedCompletionNumber: Union[Range, None] = None
  plannedSex: List[Code] = []
  criteria: List[EligibilityCriteria] = []
  plannedAge: Union[Range, None] = None
  instanceType: Literal['PopulationDefinition'] = 'PopulationDefinition'

class StudyCohort(PopulationDefinition):
  characteristics: List[Characteristic] = []
  instanceType: Literal['StudyCohort'] = 'StudyCohort'
  
class StudyDesignPopulation(PopulationDefinition):
  cohorts: List[StudyCohort] = []
  instanceType: Literal['StudyDesignPopulation'] = 'StudyDesignPopulation'
