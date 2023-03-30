from typing import List, Union
from .api_base_model import ApiBaseModel
from .code import Code
from .endpoint import Endpoint
from uuid import UUID

class Objective(ApiBaseModel):
  objectiveId: str
  objectiveDescription: str
  objectiveLevel: Union[Code, None] = None
  objectiveEndpoints: List[Endpoint] = []