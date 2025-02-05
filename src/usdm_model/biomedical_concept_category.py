from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .alias_code import AliasCode
from .comment_annotation import CommentAnnotation


class BiomedicalConceptCategory(ApiBaseModelWithIdNameLabelAndDesc):
    childIds: List[str] = []
    memberIds: List[str] = []
    code: Union[AliasCode, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["BiomedicalConceptCategory"]
