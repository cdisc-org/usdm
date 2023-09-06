from typing import Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class Timing(ApiBaseModelWithIdNameLabelAndDesc):
  type: Code
  timingValue: str
  timingRelativeToFrom: Code
  relativeFromScheduledInstanceId: Union[str, None] = None
  relativeToScheduledInstanceId: Union[str, None] = None
  timingWindowLower: Union[str, None] = None
  timingWindowUpper: Union[str, None] = None
  timingWindow: Union[str, None] = None
