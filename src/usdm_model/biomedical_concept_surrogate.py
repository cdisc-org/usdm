from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .comment_annotation import CommentAnnotation


class BiomedicalConceptSurrogate(ApiBaseModelWithIdNameLabelAndDesc):
    reference: Union[str, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["BiomedicalConceptSurrogate"]
