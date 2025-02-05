from typing import List, Literal
from .api_base_model import ApiBaseModelWithId
from .code import Code


class CommentAnnotation(ApiBaseModelWithId):
    text: str
    codes: List[Code] = []
    instanceType: Literal["CommentAnnotation"]
