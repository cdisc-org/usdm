from typing import List, Union
from .api_base_model import ApiBaseModelWithId
from .study_identifier import *
from .study_protocol_document_version import *
from .alias_code import *
from .code import Code as genericCode
from .study_design import *
from .governance_date import GovernanceDate
from .study_amendment import StudyAmendment

class StudyVersion(ApiBaseModelWithId):
  studyTitle: str
  studyVersion: str
  type: Union[genericCode, None] = None
  studyPhase: Union[AliasCode, None] = None
  documentVersion: Union[StudyProtocolDocumentVersion, None] = None
  approvedOn: List[GovernanceDate] = []
  protocolAmendments: List[StudyAmendment] = []
  businessTherapeuticAreas: List[Code] = []
  studyIdentifiers: List[StudyIdentifier] = []
  studyDesigns: List[StudyDesign] = []
  studyRationale: str
  studyAcronym: str
