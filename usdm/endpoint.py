from typing import Union
from .api_base_model import ApiBaseModel
from .code import Code
from uuid import UUID

class Endpoint(ApiBaseModel):
  endpointId: str
  endpointDescription: str
  endpointPurposeDescription: str
  endpointLevel: Union[Code, None] = None