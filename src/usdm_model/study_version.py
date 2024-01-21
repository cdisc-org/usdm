from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithId
from .study_identifier import *
from .study_protocol_document_version import *
from .alias_code import *
from .code import Code as genericCode
from .study_design import *
from .governance_date import GovernanceDate
from .study_amendment import StudyAmendment
from .study_title import StudyTitle

class StudyVersion(ApiBaseModelWithId):
  versionIdentifier: str
  rationale: str
  studyType: Union[genericCode, None] = None
  studyPhase: Union[AliasCode, None] = None
  documentVersionId: Union[str, None] = None
  dateValues: List[GovernanceDate] = []
  amendments: List[StudyAmendment] = []
  businessTherapeuticAreas: List[Code] = []
  studyIdentifiers: List[StudyIdentifier] = []
  studyDesigns: List[StudyDesign] = []
  titles: List[StudyTitle]
  instanceType: Literal['StudyVersion']
