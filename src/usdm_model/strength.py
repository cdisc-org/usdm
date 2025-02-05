from typing import Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .range import Range


class Strength(ApiBaseModelWithIdNameLabelAndDesc):
    denominator: Union[Quantity, None] = None
    numerator: Union[Quantity, Range, None] = None
    instanceType: Literal["Strength"]
