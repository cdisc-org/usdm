from typing import Literal
from .api_base_model import ApiBaseModelWithId
from .code import Code


class ResponseCode(ApiBaseModelWithId):
    isEnabled: bool
    code: Code
    instanceType: Literal["ResponseCode"]
