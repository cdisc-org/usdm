from typing import List, Union
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
from .investigational_intervention import InvestigationalIntervention
from .study_arm import StudyArm
from .study_epoch import StudyEpoch
from .study_element import StudyElement
from .study_design_population import StudyDesignPopulation
from .objective import Objective
from .schedule_timeline import ScheduleTimeline
from .estimand import Estimand
from .study_protocol_document_version import StudyProtocolDocumentVersion
from .eligibility_criteria import EligibilityCriteria

class StudyDesign(ApiBaseModelWithIdNameLabelAndDesc):
  trialIntentTypes: List[Code] = []
  trialTypes: List[Code] = []
  therapeuticAreas: List[Code] = []
  interventionModel: Code
  encounters: List[Encounter] = []
  activities: List[Activity] = []
  biomedicalConcepts: List[BiomedicalConcept] = []
  bcCategories: List[BiomedicalConceptCategory] = []
  bcSurrogates: List[BiomedicalConceptSurrogate] = []
  studyArms: List[StudyArm]
  studyCells: List[StudyCell]
  studyDesignBlindingScheme: Union[AliasCode, None] = None
  studyDesignRationale: str
  studyEpochs: List[StudyEpoch]
  studyElements: List[StudyElement] = []
  studyEstimands: List[Estimand] = []
  studyIndications: List[Indication] = []
  studyInvestigationalInterventions: List[InvestigationalIntervention] = []
  studyObjectives: List[Objective] = []
  studyPopulations: List[StudyDesignPopulation] = []
  studyScheduleTimelines: List[ScheduleTimeline] = []
  documentVersion: Union[StudyProtocolDocumentVersion, None] = None
  studyEligibilityCritieria: List[EligibilityCriteria] = []    
  