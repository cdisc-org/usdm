from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from typing import Literal

class AnalysisPopulation(ApiBaseModelWithIdNameLabelAndDesc):
  text: str
  instanceType: Literal['AnalysisPopulation'] = 'AnalysisPopulation'
