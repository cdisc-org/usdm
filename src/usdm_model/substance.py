from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .strength import Strength
from .code import Code


class Substance(ApiBaseModelWithIdNameLabelAndDesc):
    codes: List[Code] = []
    strengths: List[Strength] = []  # Not in API
    referenceSubstance: Union["Substance", None] = None
    instanceType: Literal["Substance"]
