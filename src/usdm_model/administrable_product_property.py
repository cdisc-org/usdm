from typing import Union, Literal
from .api_base_model import ApiBaseModelWithIdAndName
from .quantity_range import Quantity
from .code import Code


class AdministrableProductProperty(ApiBaseModelWithIdAndName):
    text: str
    type: Code
    quantity: Union[Quantity, None] = None
    instanceType: Literal["AdministrableProductProperty"]
