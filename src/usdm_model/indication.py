from typing import List
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class Indication(ApiBaseModelWithIdNameLabelAndDesc):
  codes: List[Code] = []
