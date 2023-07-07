from typing import List
from .api_base_model import ApiIdModel
from .code import Code

class ResponseCode(ApiIdModel):
  responseCodeEnabled: bool
  code: Code
