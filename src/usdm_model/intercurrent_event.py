from typing import Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc

class IntercurrentEvent(ApiBaseModelWithIdNameLabelAndDesc):
  strategy: str
  instanceType: Literal['IntercurrentEvent']
