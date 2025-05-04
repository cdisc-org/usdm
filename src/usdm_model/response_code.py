from typing import Literal
from .api_base_model import ApiBaseModelWithIdNameAndLabel
from .code import Code


class ResponseCode(ApiBaseModelWithIdNameAndLabel):
    isEnabled: bool
    code: Code
    instanceType: Literal["ResponseCode"]
