from typing import Literal
from .api_base_model import ApiBaseModelWithId


class Masking(ApiBaseModelWithId):
    description: str
    instanceType: Literal["Masking"]
