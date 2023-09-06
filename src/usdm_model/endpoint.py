from typing import Union
from .api_base_model import ApiBaseModelWithIdAndDesc
from .code import Code

class Endpoint(ApiBaseModelWithIdAndDesc):
  purpose: str
  endpointLevel: Union[Code, None] = None
