from .api_base_model import ApiBaseModelWithIdAndDesc
from .code import Code
from typing import Literal

class Masking(ApiBaseModelWithIdAndDesc):
  role: Code
  instanceType: Literal['Masking'] = 'Masking'
