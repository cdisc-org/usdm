from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .comment_annotation import CommentAnnotation


class StudyEpoch(ApiBaseModelWithIdNameLabelAndDesc):
    type: Code
    previousId: Union[str, None] = None
    nextId: Union[str, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["StudyEpoch"]
