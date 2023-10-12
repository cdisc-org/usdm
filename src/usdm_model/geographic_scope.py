from .api_base_model import ApiBaseModelWithId
from .code import Code

class GeographicScope(ApiBaseModelWithId):
  type: Code
  code: Code
