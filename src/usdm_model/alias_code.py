from typing import List
from .api_base_model import ApiBaseModelWithId
from .code import Code

class AliasCode(ApiBaseModelWithId):
  standardCode: Code
  standardCodeAliases: List[Code] = []
