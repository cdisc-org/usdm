from typing import Literal, Union
from .api_base_model import ApiBaseModelWithId
from .quantity import Quantity

class AdministrationDuration(ApiBaseModelWithId):
  quantity:	Union[Quantity, None] = None
  description: str
  durationWillVary: bool
  reasonDurationWillVary:	str
  instanceType: Literal['AdministrationDuration']
