from typing import Union
from .api_base_model import ApiIdModel
from .code import Code

class Endpoint(ApiIdModel):
  endpointDescription: str
  endpointPurposeDescription: str
  endpointLevel: Union[Code, None] = None