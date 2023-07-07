from typing import List
from .api_base_model import ApiBaseModel
from .code import Code

from uuid import UUID

class AliasCode(ApiBaseModel):
  standardCode: Code
  standardCodeAliases: List[Code] = []
