from typing import Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc

class StudySite(ApiBaseModelWithIdNameLabelAndDesc):
  instanceType: Literal['StudySite']
