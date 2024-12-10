from typing import List, Literal, Union
from .activity import Activity
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .alias_code import AliasCode
from .biomedical_concept import BiomedicalConcept
from .biomedical_concept_category import BiomedicalConceptCategory
from .biomedical_concept_surrogate import BiomedicalConceptSurrogate
from .code import Code
from .encounter import Encounter
from .study_cell import StudyCell
from .indication import Indication
from .study_intervention import StudyIntervention
from .study_arm import StudyArm
from .study_epoch import StudyEpoch
from .study_element import StudyElement
from .population_definition import StudyDesignPopulation
from .analysis_population import AnalysisPopulation
from .objective import Objective
from .schedule_timeline import ScheduleTimeline
from .estimand import Estimand
from .syntax_template_dictionary import SyntaxTemplateDictionary
from .condition import Condition
from .comment_annotation import CommentAnnotation

class StudyDesign(ApiBaseModelWithIdNameLabelAndDesc):
  trialIntentTypes: List[Code] = []
  trialTypes: List[Code] = []
  therapeuticAreas: List[Code] = []
  characteristics: List[Code] = []
  interventionModel: Code
  encounters: List[Encounter] = []
  activities: List[Activity] = []
  biomedicalConcepts: List[BiomedicalConcept] = []
  bcCategories: List[BiomedicalConceptCategory] = []
  bcSurrogates: List[BiomedicalConceptSurrogate] = []
  arms: List[StudyArm]
  studyCells: List[StudyCell]
  blindingSchema: Union[AliasCode, None] = None
  rationale: str
  epochs: List[StudyEpoch]
  elements: List[StudyElement] = []
  estimands: List[Estimand] = []
  indications: List[Indication] = []
  studyInterventions: List[StudyIntervention] = []
  objectives: List[Objective] = []
  population: Union[StudyDesignPopulation, None] = None
  analysisPopulations: List[AnalysisPopulation] = []
  scheduleTimelines: List[ScheduleTimeline] = []
  documentVersionIds: List[str] = []
  dictionaries: List[SyntaxTemplateDictionary] = []
  conditions: List[Condition] = []
  notes: List[CommentAnnotation] = []
  instanceType: Literal['StudyDesign']

  def main_timeline(self):
    return next((item for item in self.scheduleTimelines if item.mainTimeline), None)