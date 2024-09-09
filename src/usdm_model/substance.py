from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .strength import Strength
from .code import Code

class Substance(ApiBaseModelWithIdNameLabelAndDesc):
  code: Union[Code, None] = None
  strengths: List[Strength] = [] # Not in API
  referenceSubstance: Union['Substance', None] = None
  instanceType: Literal['Substance']
