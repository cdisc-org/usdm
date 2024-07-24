from typing import List, Literal
from .api_base_model import ApiBaseModelWithId
from .code import Code
from .governance_date import GovernanceDate
from .narrative_content import NarrativeContent
from .comment_annotation import CommentAnnotation

class StudyDefinitionDocumentVersion(ApiBaseModelWithId):
  version: str
  status: Code
  dateValues: List[GovernanceDate] = []
  contents: List[NarrativeContent] = []
  childIds: List[str] = []
  notes: List[CommentAnnotation] = []
  instanceType: Literal['StudyDefinitionDocumentVersion']
