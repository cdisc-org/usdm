from .api_base_model import ApiBaseModelWithId
from .quantity import Quantity
from typing import Literal

class AdministrationDuration(ApiBaseModelWithId):
  quantity:	Quantity
  description: str
  durationWillVary: bool
  reasonDurationWillVary:	str
  instanceType: Literal['AdministrationDuration']
