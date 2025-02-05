from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .comment_annotation import CommentAnnotation


class Procedure(ApiBaseModelWithIdNameLabelAndDesc):
    procedureType: str
    code: Code
    studyInterventionId: Union[str, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["Procedure"]
