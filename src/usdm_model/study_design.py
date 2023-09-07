from typing import List, Union
from .activity import Activity
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .alias_code import AliasCode
from .biomedical_concept import BiomedicalConcept
from .biomedical_concept_category import BiomedicalConceptCategory
from .biomedical_concept_surrogate import BiomedicalConceptSurrogate
from .code import Code
from .content import Content
from .encounter import Encounter
from .study_cell import StudyCell
from .indication import Indication
from .investigational_intervention import InvestigationalIntervention
from .study_arm import StudyArm
from .study_epoch import StudyEpoch
from .study_element import StudyElement
from .study_design_population import StudyDesignPopulation
from .objective import Objective
from .schedule_timeline import ScheduleTimeline
from .estimand import Estimand

class StudyDesign(ApiBaseModelWithIdNameLabelAndDesc):
  trialIntentTypes: List[Code] = []
  trialTypes: List[Code] = []
  interventionModel: Code
  studyCells: List[StudyCell]
  studyIndications: List[Indication] = []
  studyInvestigationalInterventions: List[InvestigationalIntervention] = []
  studyPopulations: List[StudyDesignPopulation] = []
  studyObjectives: List[Objective] = []
  studyScheduleTimelines: List[ScheduleTimeline] = []
  therapeuticAreas: List[Code] = []
  studyEstimands: List[Estimand] = []
  encounters: List[Encounter] = []
  activities: List[Activity] = []
  studyDesignRationale: str
  studyDesignBlindingScheme: Union[AliasCode, None] = None
  biomedicalConcepts: List[BiomedicalConcept] = []
  bcCategories: List[BiomedicalConceptCategory] = []
  bcSurrogates: List[BiomedicalConceptSurrogate] = []
  studyArms: List[StudyArm]
  studyEpochs: List[StudyEpoch]
  studyElements: List[StudyElement] = []
  contents: List[Content] = []
