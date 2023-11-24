from typing import Union
from .api_base_model import ApiBaseModelWithId
from .code import Code

class Range(ApiBaseModelWithId):
  minValue: float
  maxValue: float
  unit: Union[Code, None] = None
  isApproximate: bool
