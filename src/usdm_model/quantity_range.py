from typing import Literal, Union
from .api_base_model import ApiBaseModelWithId
from .alias_code import AliasCode


class QuantityRange(ApiBaseModelWithId):
    pass


class Quantity(QuantityRange):
    value: float
    unit: Union[AliasCode, None] = None
    instanceType: Literal["Quantity"]


class Range(QuantityRange):
    minValue: Quantity
    maxValue: Quantity
    isApproximate: bool
    instanceType: Literal["Range"]
