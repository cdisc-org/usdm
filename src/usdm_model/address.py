from typing import Literal, Union, List
from .api_base_model import ApiBaseModelWithId
from .code import Code


class Address(ApiBaseModelWithId):
    text: Union[str, None] = None
    lines: List[str] = []
    city: Union[str, None] = None
    district: Union[str, None] = None
    state: Union[str, None] = None
    postalCode: Union[str, None] = None
    country: Union[Code, None] = None
    instanceType: Literal["Address"]
