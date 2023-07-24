from typing import List, Union
from .api_base_model import ApiDescriptionModel
from .code import Code
from .endpoint import Endpoint

class Objective(ApiDescriptionModel):
  objectiveLevel: Union[Code, None] = None
  objectiveEndpoints: List[Endpoint] = []