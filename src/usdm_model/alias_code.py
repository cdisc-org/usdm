from typing import List
from .api_base_model import ApiIdModel
from .code import Code

class AliasCode(ApiIdModel):
  standardCode: Code
  standardCodeAliases: List[Code] = []
