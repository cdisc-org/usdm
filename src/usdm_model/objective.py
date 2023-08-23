from typing import List, Union
from .api_base_model import ApiNameDescriptionModel
from .code import Code
from .endpoint import Endpoint

class Objective(ApiNameDescriptionModel):
  objectiveLevel: Union[Code, None] = None
  objectiveEndpoints: List[Endpoint] = []