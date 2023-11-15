from .api_base_model import ApiBaseModelWithId
from .code import Code

class Quantity(ApiBaseModelWithId):
  unit: Code
  value: float
