from typing import Union
from .api_base_model import ApiBaseModel

class IntercurrentEvent(ApiBaseModel):
  intercurrentEventStrategy: str
  intercurrentEventName: str
  intercurrentEventDescription: Union[str, None] = None