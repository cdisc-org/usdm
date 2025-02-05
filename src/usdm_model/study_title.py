from typing import Literal
from .api_base_model import ApiBaseModelWithId
from .code import Code


class StudyTitle(ApiBaseModelWithId):
    text: str
    type: Code
    instanceType: Literal["StudyTitle"]
