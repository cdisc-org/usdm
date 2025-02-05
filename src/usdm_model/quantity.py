from typing import Literal, Union
from .api_base_model import ApiBaseModelWithId
from .alias_code import AliasCode


class Quantity(ApiBaseModelWithId):
    value: float
    unit: Union[AliasCode, None] = None
    instanceType: Literal["Quantity"]
