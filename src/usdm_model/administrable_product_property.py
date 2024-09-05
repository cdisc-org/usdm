from typing import Literal
from .api_base_model import ApiBaseModelWithIdAndName
from .quantity import Quantity
from .code import Code

class AdministrableProductProperty(ApiBaseModelWithIdAndName):
  text: str
  type: Code
  quantity: Quantity
  instanceType: Literal['AdministrableProductProperty']
