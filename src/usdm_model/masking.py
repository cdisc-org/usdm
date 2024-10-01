from .api_base_model import ApiBaseModelWithIdAndDesc
from typing import Literal

class Masking(ApiBaseModelWithIdAndDesc):
  instanceType: Literal['Masking']
