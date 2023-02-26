from typing import List, Union
from .api_base_model import ApiBaseModel
from .code import Code

from uuid import UUID

class AliasCode(ApiBaseModel):
  aliasCodeId: str
  standardCode: Code
  standardCodeAliases: List[Code] = []
