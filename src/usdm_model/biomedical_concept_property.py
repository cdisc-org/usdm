from typing import List, Literal
from .alias_code import AliasCode
from .api_base_model import ApiBaseModelWithIdNameAndLabel
from .response_code import ResponseCode
from .comment_annotation import CommentAnnotation


class BiomedicalConceptProperty(ApiBaseModelWithIdNameAndLabel):
    isRequired: bool
    isEnabled: bool
    datatype: str
    responseCodes: List[ResponseCode] = []
    code: AliasCode
    notes: List[CommentAnnotation] = []
    instanceType: Literal["BiomedicalConceptProperty"]
