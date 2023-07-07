from typing import Union
from .api_base_model import ApiIdModel

class IntercurrentEvent(ApiIdModel):
  intercurrentEventStrategy: str
  intercurrentEventName: str
  intercurrentEventDescription: Union[str, None] = None