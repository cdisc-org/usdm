from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class Indication(ApiBaseModelWithIdNameLabelAndDesc):
  codes: List[Code] = []
  isRareDisease: bool
  instanceType: Literal['Indication'] = 'Indication'
