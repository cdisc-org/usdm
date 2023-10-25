from typing import List
from .api_base_model import ApiBaseModelWithId
from .code import Code
from .governance_date import GovernanceDate
from .narrative_content import NarrativeContent

class StudyProtocolDocumentVersion(ApiBaseModelWithId):
  briefTitle: str
  officialTitle: str
  publicTitle: str
  scientificTitle: str
  protocolVersion: str
  protocolStatus: Code
  dateValues: List[GovernanceDate] = []
  contents: List[NarrativeContent] = []
  childrenIds: List[str] = []
