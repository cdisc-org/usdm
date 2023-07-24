from typing import Union
from .api_base_model import ApiDescriptionModel
from .code import Code

class Endpoint(ApiDescriptionModel):
  endpointPurposeDescription: str
  endpointLevel: Union[Code, None] = None