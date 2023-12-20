from typing import Literal, Union
from .api_base_model import ApiBaseModelWithId
from .code import Code

class Quantity(ApiBaseModelWithId):
  value: float
  unit: Union[Code, None] = None
  instanceType: Literal['Quantity'] = 'Quantity'
