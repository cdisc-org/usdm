from typing import Literal, Union
from .api_base_model import ApiBaseModelWithId
from .alias_code import AliasCode


class Range(ApiBaseModelWithId):
    minValue: float
    maxValue: float
    unit: Union[AliasCode, None] = None
    isApproximate: bool
    instanceType: Literal["Range"]
