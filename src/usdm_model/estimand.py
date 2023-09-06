from typing import List, Union
from .api_base_model import ApiBaseModelWithId
from .analysis_population import AnalysisPopulation
from .intercurrent_event import IntercurrentEvent

class Estimand(ApiBaseModelWithId):
  summaryMeasure: str
  analysisPopulation: AnalysisPopulation
  treatmentId: Union[str, None] = None
  variableOfInterestId: Union[str, None] = None
  intercurrentEvents: List[IntercurrentEvent] = []
