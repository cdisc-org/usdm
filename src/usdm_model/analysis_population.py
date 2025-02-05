from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .comment_annotation import CommentAnnotation


class AnalysisPopulation(ApiBaseModelWithIdNameLabelAndDesc):
    text: str
    subsetOfIds: List[str] = []
    notes: List[CommentAnnotation] = []
    instanceType: Literal["AnalysisPopulation"]
