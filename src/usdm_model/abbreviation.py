from typing import List, Literal
from pydantic import Field
from .api_base_model import ApiBaseModelWithId
from .comment_annotation import CommentAnnotation


class Abbreviation(ApiBaseModelWithId):
    abbreviatedText: str = Field(min_length=1)
    expandedText: str = Field(min_length=1)
    notes: List[CommentAnnotation] = []
    instanceType: Literal["Abbreviation"]
