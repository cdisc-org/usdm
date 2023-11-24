from typing import Union
from .api_base_model import ApiBaseModelWithId
from .code import Code

class Quantity(ApiBaseModelWithId):
  value: float
  unit: Union[Code, None] = None
