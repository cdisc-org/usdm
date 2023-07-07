from typing import List, Union
from .api_base_model import ApiIdModel
from .code import Code
from .endpoint import Endpoint

class Objective(ApiIdModel):
  objectiveDescription: str
  objectiveLevel: Union[Code, None] = None
  objectiveEndpoints: List[Endpoint] = []