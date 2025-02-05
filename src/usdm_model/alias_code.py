from typing import List, Literal
from .api_base_model import ApiBaseModelWithId
from .code import Code


class AliasCode(ApiBaseModelWithId):
    standardCode: Code
    standardCodeAliases: List[Code] = []
    instanceType: Literal["AliasCode"]
