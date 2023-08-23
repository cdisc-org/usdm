from typing import List
from .api_base_model import ApiNameDescriptionModel
from .code import Code

class Indication(ApiNameDescriptionModel):
  codes: List[Code] = []
