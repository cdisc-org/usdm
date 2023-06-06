from typing import Union
from .api_base_model import ApiBaseModel
from .code import Code

class Endpoint(ApiBaseModel):
  endpointId: str
  endpointDescription: str
  endpointPurposeDescription: str
  endpointLevel: Union[Code, None] = None