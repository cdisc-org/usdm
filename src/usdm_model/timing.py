from typing import Union
from .api_base_model import ApiNameDescriptionModel
from .code import Code

class Timing(ApiNameDescriptionModel):
  timingType: Code
  timingValue: str
  timingRelativeToFrom: Code
  relativeFromScheduledInstanceId: Union[str, None] = None
  relativeToScheduledInstanceId: Union[str, None] = None
  timingWindowLower: Union[str, None] = None
  timingWindowUpper: Union[str, None] = None
  timingWindow: Union[str, None] = None
  label: Union[str, None] = None