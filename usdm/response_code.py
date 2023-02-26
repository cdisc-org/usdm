from typing import List
from .api_base_model import ApiBaseModel
from .code import Code

class ResponseCode(ApiBaseModel):
  responseCodeId: str
  responseCodeEnabled: bool
  code: Code
