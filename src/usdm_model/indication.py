from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .comment_annotation import CommentAnnotation


class Indication(ApiBaseModelWithIdNameLabelAndDesc):
    codes: List[Code] = []
    isRareDisease: bool
    notes: List[CommentAnnotation] = []
    instanceType: Literal["Indication"]
