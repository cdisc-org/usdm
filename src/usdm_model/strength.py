from typing import Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .range import Range


class Strength(ApiBaseModelWithIdNameLabelAndDesc):
    denominator: Union[Quantity, None] = None
    numeratorQuantity: Union[Quantity, None] = None
    numeratorRange: Union[Range, None] = None
    instanceType: Literal["Strength"]
