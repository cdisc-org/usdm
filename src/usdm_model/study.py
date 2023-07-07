from typing import List, Union
from .api_base_model import CoreModel
from .study_identifier import *
from .study_protocol_version import *
from .alias_code import *
from .code import Code as genericCode
from .study_design import *
from uuid import UUID

class Study(CoreModel):
  uuid: Union[UUID, None] = None
  studyTitle: str
  studyVersion: str
  studyType: Union[genericCode, None] = None
  studyPhase: Union[AliasCode, None] = None
  businessTherapeuticAreas: List[Code] = []
  studyIdentifiers: List[StudyIdentifier] = []
  studyProtocolVersions: List[StudyProtocolVersion] = []
  studyDesigns: List[StudyDesign] = []
  studyRationale: str
  studyAcronym: str
