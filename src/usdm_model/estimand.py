from typing import List, Union
from .api_base_model import ApiIdModel
from .analysis_population import AnalysisPopulation
from .intercurrent_event import IntercurrentEvent

class Estimand(ApiIdModel):
  summaryMeasure: str
  analysisPopulation: AnalysisPopulation
  treatmentId: Union[str, None] = None
  variableOfInterestId: Union[str, None] = None
  intercurrentEvents: List[IntercurrentEvent] = []
