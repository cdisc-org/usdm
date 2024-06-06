from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .analysis_population import AnalysisPopulation
from .intercurrent_event import IntercurrentEvent
from .comment_annotation import CommentAnnotation

class Estimand(ApiBaseModelWithIdNameLabelAndDesc):
  summaryMeasure: str
  analysisPopulation: AnalysisPopulation
  interventionId: str
  variableOfInterestId: str
  intercurrentEvents: List[IntercurrentEvent]
  notes: List[CommentAnnotation] = []
  instanceType: Literal['Estimand']
