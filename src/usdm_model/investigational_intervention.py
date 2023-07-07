from typing import List, Union
from .api_base_model import ApiBaseModel
from .code import Code

class InvestigationalIntervention(ApiBaseModel):
  interventionDescription: str
  codes: List[Code] = []
