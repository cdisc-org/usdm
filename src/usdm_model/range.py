from typing import Literal
from .api_base_model import ApiBaseModelWithId
from .quantity import Quantity


class Range(ApiBaseModelWithId):
    minValue: Quantity
    maxValue: Quantity
    isApproximate: bool
    instanceType: Literal["Range"]
