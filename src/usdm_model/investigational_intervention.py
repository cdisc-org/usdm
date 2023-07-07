from typing import List, Union
from .api_base_model import ApiIdModel
from .code import Code

class InvestigationalIntervention(ApiIdModel):
  interventionDescription: str
  codes: List[Code] = []
