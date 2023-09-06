from datetime import date
from typing import Union
from .api_base_model import ApiBaseModelWithId
from .code import Code

class StudyProtocolVersion(ApiBaseModelWithId):
  briefTitle: str
  officialTitle: str
  publicTitle: str
  scientificTitle: str
  protocolVersion: str
  protocolAmendment: Union[str, None] = None
  protocolEffectiveDate: date
  protocolStatus: Code
