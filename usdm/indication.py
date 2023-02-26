from typing import List, Union
from .api_base_model import ApiBaseModel
from .code import Code
from uuid import UUID

class Indication(ApiBaseModel):
  indicationId: str
  indicationDescription: str
  codes: List[Code] = []
