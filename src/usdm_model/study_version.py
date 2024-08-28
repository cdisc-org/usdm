from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithId
from .identifier import *
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
  studyIdentifiers: List[StudyIdentifier]
  referenceIdentifiers: List[ReferenceIdentifier] = []
  studyDesigns: List[StudyDesign] = []
  titles: List[StudyTitle]
  criteria: List[EligibilityCriterion] = [] # Not in API
  narrativeContentItems: List[NarrativeContentItem] = []
  abbreviations: List[Abbreviation] = []
  notes: List[CommentAnnotation] = []
  instanceType: Literal['StudyVersion']

  def get_title(self, title_type):
    for title in self.titles:
      if title.type.decode == title_type:
        return title
    return None

  def sponsor_identifier(self):
    for identifier in self.studyIdentifiers:
      if identifier.scope.organizationType.code == 'C70793':
        return identifier
    return None

  def phase(self):
    return self.studyPhase.standardCode