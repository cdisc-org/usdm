from typing import List, Literal
from .api_base_model import ApiBaseModelWithId
from .analysis_population import AnalysisPopulation
from .intercurrent_event import IntercurrentEvent

class Estimand(ApiBaseModelWithId):
  summaryMeasure: str
  analysisPopulation: AnalysisPopulation
  treatmentId: str
  variableOfInterestId: str
  intercurrentEvents: List[IntercurrentEvent]
  instanceType: Literal['Estimand']
