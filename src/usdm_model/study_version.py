from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithId
from .study_identifier import *
from .study_definition_document_version import *
from .alias_code import *
from .code import Code as genericCode
from .study_design import *
from .governance_date import GovernanceDate
from .study_amendment import StudyAmendment
from .study_title import StudyTitle
from .eligibility_criterion import EligibilityCriterion
from .narrative_content import NarrativeContentItem
from .comment_annotation import CommentAnnotation
from .abbreviation import Abbreviation

class StudyVersion(ApiBaseModelWithId):
  versionIdentifier: str
  rationale: str
  studyType: Union[genericCode, None] = None
  studyPhase: Union[AliasCode, None] = None
  documentVersionIds: List[str] = []
  dateValues: List[GovernanceDate] = []
  amendments: List[StudyAmendment] = []
  businessTherapeuticAreas: List[Code] = []
  studyIdentifiers: List[StudyIdentifier] = []
  studyDesigns: List[StudyDesign] = []
  titles: List[StudyTitle]
  criteria: List[EligibilityCriterion]
  narrativeContentItems: List[NarrativeContentItem] = []
  abbreviations: List[Abbreviation] = []
  notes: List[CommentAnnotation] = []
  instanceType: Literal['StudyVersion']
