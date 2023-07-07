from typing import List
from .api_base_model import ApiIdModel
from .code import Code

class Indication(ApiIdModel):
  indicationDescription: str
  codes: List[Code] = []
