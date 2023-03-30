from typing import List, Union
from .api_base_model import ApiBaseModel
from .code import Code
from uuid import UUID

class InvestigationalIntervention(ApiBaseModel):
  investigationalInterventionId: str
  interventionDescription: str
  codes: List[Code] = []
