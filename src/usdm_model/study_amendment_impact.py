from typing import Literal, Union, List
from .api_base_model import ApiBaseModelWithId
from .code import Code
from .comment_annotation import CommentAnnotation


class StudyAmendmentImpact(ApiBaseModelWithId):
    type: Code
    text: str
    isSubstantial: bool
    notes: List[CommentAnnotation] = []
    instanceType: Literal["StudyAmendmentImpact"]
