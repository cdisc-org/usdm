from typing import List
from .api_base_model import ApiIdModel
from .code import Code

from uuid import UUID

class AliasCode(ApiIdModel):
  standardCode: Code
  standardCodeAliases: List[Code] = []
