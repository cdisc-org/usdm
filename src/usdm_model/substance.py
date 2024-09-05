from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .strength import Strength
from .code import Code

class Substance(ApiBaseModelWithIdNameLabelAndDesc):
  code: Code
  strengths: List[Strength]
  referenceSubstance: Union['Substance', None] = None
  instanceType: Literal['Substance']
