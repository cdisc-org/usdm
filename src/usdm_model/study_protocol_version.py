from datetime import date
from typing import Union
from .api_base_model import ApiIdModel
from .code import Code
from uuid import UUID

class StudyProtocolVersion(ApiIdModel):
  briefTitle: str
  officialTitle: str
  publicTitle: str
  scientificTitle: str
  protocolVersion: str
  protocolAmendment: Union[str, None] = None
  protocolEffectiveDate: date
  protocolStatus: Code
