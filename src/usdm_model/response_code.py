from .api_base_model import ApiBaseModelWithId
from .code import Code

class ResponseCode(ApiBaseModelWithId):
  responseCodeEnabled: bool
  code: Code
