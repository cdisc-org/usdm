from typing import Literal
from .api_base_model import ApiBaseModelWithId


class Masking(ApiBaseModelWithId):
    text: str
    isMasked: bool
    instanceType: Literal["Masking"]
