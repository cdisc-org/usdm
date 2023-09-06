from typing import List
from .api_base_model import ApiBaseModelWithIdAndDesc
from .code import Code

class InvestigationalIntervention(ApiBaseModelWithIdAndDesc):
  codes: List[Code] = []
