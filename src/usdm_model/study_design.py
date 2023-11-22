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
from .study_intervention import StudyIntervention
from .study_arm import StudyArm
from .study_epoch import StudyEpoch
from .study_element import StudyElement
from .study_design_population import StudyDesignPopulation
from .objective import Objective
from .schedule_timeline import ScheduleTimeline
from .estimand import Estimand
from .study_protocol_document_version import StudyProtocolDocumentVersion
from .syntax_template_dictionary import SyntaxTemplateDictionary

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
  scheduleTimelines: List[ScheduleTimeline] = []
  documentVersion: Union[StudyProtocolDocumentVersion, None] = None
  dictionaries: List[SyntaxTemplateDictionary] = []