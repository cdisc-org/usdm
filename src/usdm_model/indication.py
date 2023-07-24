from typing import List
from .api_base_model import ApiDescriptionModel
from .code import Code

class Indication(ApiDescriptionModel):
  codes: List[Code] = []
