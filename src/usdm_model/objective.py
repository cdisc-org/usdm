from typing import List, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .endpoint import Endpoint

class Objective(ApiBaseModelWithIdNameLabelAndDesc):
  objectiveLevel: Union[Code, None] = None
  objectiveEndpoints: List[Endpoint] = []