from typing import Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity_range import Quantity, Range


class Strength(ApiBaseModelWithIdNameLabelAndDesc):
    numerator: Union[Quantity, Range]
    denominator: Union[Quantity, None] = None
    instanceType: Literal["Strength"]
