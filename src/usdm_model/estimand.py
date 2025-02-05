from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .intercurrent_event import IntercurrentEvent
from .comment_annotation import CommentAnnotation


class Estimand(ApiBaseModelWithIdNameLabelAndDesc):
    populationSummary: str
    analysisPopulationId: str
    interventionIds: List[str]
    variableOfInterestId: str
    intercurrentEvents: List[IntercurrentEvent]
    notes: List[CommentAnnotation] = []
    instanceType: Literal["Estimand"]
