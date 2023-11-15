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
  versionIdentifier: str
  rationale: str
  studyAcronym: str
  type: Union[genericCode, None] = None
  studyPhase: Union[AliasCode, None] = None
  documentVersionId: Union[str, None] = None
  dateValues: List[GovernanceDate] = []
  amendments: List[StudyAmendment] = []
  businessTherapeuticAreas: List[Code] = []
  studyIdentifiers: List[StudyIdentifier] = []
  studyDesigns: List[StudyDesign] = []
