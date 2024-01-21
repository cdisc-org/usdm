from typing import Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class Timing(ApiBaseModelWithIdNameLabelAndDesc):
  type: Code
  value: str
  relativeToFrom: Code
  relativeFromScheduledInstanceId: Union[str, None] = None
  relativeToScheduledInstanceId: Union[str, None] = None
  windowLower: Union[str, None] = None
  windowUpper: Union[str, None] = None
  window: Union[str, None] = None
  instanceType: Literal['Timing']
