from typing import List, Union
from .activity import Activity
from .api_base_model import ApiBaseModel
from .alias_code import AliasCode
from .biomedical_concept import BiomedicalConcept
from .biomedical_concept_category import BiomedicalConceptCategory
from .biomedical_concept_surrogate import BiomedicalConceptSurrogate
from .code import Code
from .encounter import Encounter
from .study_cell import StudyCell
from .indication import Indication
from .investigational_intervention import InvestigationalIntervention
from .study_design_population import StudyDesignPopulation
from .objective import Objective
from .schedule_timeline import ScheduleTimeline
from .workflow import Workflow
from .workflow_item import WorkflowItem
from .estimand import Estimand
import pandas as pd

class StudyDesign(ApiBaseModel):
  studyDesignId: str
  studyDesignName: str
  studyDesignDescription: str
  trialIntentTypes: List[Code] = []
  trialType: List[Code] = []
  interventionModel: Code
  studyCells: List[StudyCell] = []
  studyIndications: List[Indication] = []
  studyInvestigationalInterventions: List[InvestigationalIntervention] = []
  studyStudyDesignPopulations: List[StudyDesignPopulation] = []
  studyObjectives: List[Objective] = []
  studyScheduleTimelines: List[ScheduleTimeline] = []
  therapeuticAreas: List[Code] = []
  studyEstimands: List[Estimand] = []
  encounters: List[Encounter] = []
  activities: List[Activity] = []
  studyDesignRationale: str
  studyDesignBlindingScheme: AliasCode = None
  biomedicalConcepts: List[BiomedicalConcept] = []
  bcCategories: List[BiomedicalConceptCategory] = []
  bcSurrogates: List[BiomedicalConceptSurrogate] = []
