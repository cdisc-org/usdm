from typing import Union
from .api_base_model import ApiBaseModel
from .code import Code

class Endpoint(ApiBaseModel):
  endpointDescription: str
  endpointPurposeDescription: str
  endpointLevel: Union[Code, None] = None