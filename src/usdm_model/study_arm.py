from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .comment_annotation import CommentAnnotation


class StudyArm(ApiBaseModelWithIdNameLabelAndDesc):
    type: Code
    dataOriginDescription: str
    dataOriginType: Code
    populationIds: List[str] = []
    notes: List[CommentAnnotation] = []
    instanceType: Literal["StudyArm"]
