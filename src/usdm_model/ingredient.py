from typing import Literal
from .api_base_model import ApiBaseModelWithId
from .substance import Substance
from .code import Code


class Ingredient(ApiBaseModelWithId):
    role: Code
    substance: Substance
    instanceType: Literal["Ingredient"]
