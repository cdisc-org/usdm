from typing import List, Literal
from .api_base_model import ApiBaseModelWithId
from .code import Code
from .governance_date import GovernanceDate
from .narrative_content import NarrativeContent

class StudyProtocolDocumentVersion(ApiBaseModelWithId):
  protocolVersion: str
  protocolStatus: Code
  dateValues: List[GovernanceDate] = []
  contents: List[NarrativeContent] = []
  childIds: List[str] = []
  instanceType: Literal['StudyProtocolDocumentVersion']
