from typing import List
from .api_base_model import ApiBaseModel
from .code import Code

class Indication(ApiBaseModel):
  indicationId: str
  indicationDescription: str
  codes: List[Code] = []
