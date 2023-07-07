from typing import List, Union
from .api_base_model import ApiIdModel
from .analysis_population import AnalysisPopulation
from .intercurrent_event import IntercurrentEvent

class Estimand(ApiIdModel):
  summaryMeasure: str
  analysisPopulation: AnalysisPopulation
  treatment: Union[str, None] = None
  variableOfInterest: Union[str, None] = None
  intercurrentEvents: List[IntercurrentEvent] = []
