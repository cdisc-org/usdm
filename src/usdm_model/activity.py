from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .procedure import Procedure
from .comment_annotation import CommentAnnotation


class Activity(ApiBaseModelWithIdNameLabelAndDesc):
    previousId: Union[str, None] = None
    nextId: Union[str, None] = None
    childIds: List[str] = []
    definedProcedures: List[Procedure] = []
    biomedicalConceptIds: List[str] = []
    bcCategoryIds: List[str] = []
    bcSurrogateIds: List[str] = []
    timelineId: Union[str, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["Activity"]
