from .api_base_model import ApiBaseModelWithId
from .code import Code

class Range(ApiBaseModelWithId):
  minValue: float
  maxValue: float
  isApproximate: bool
  unit: Code
