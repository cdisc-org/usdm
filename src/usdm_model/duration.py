from typing import Literal, Union
from .api_base_model import ApiBaseModelWithId
from .quantity_range import Quantity, Range


class Duration(ApiBaseModelWithId):
    text: Union[str, None] = None
    quantity: Union[Quantity, Range, None] = None
    durationWillVary: bool
    reasonDurationWillVary: Union[str, None] = None
    instanceType: Literal["Duration"]
