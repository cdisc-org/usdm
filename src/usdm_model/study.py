from typing import List, Literal, Union
from pydantic import constr
from .api_base_model import ApiBaseModel
from .study_protocol_document import StudyProtocolDocument
from .study_version import StudyVersion
from uuid import UUID

class Study(ApiBaseModel):
  id: Union[UUID, None] = None
  name: str = constr(min_length=1)
  description: Union[str, None] = None
  label: Union[str, None] = None
  versions: List[StudyVersion] = []
  documentedBy: Union[StudyProtocolDocument, None] = None
  instanceType: Literal['Study']
