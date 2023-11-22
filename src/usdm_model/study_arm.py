from typing import List
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class StudyArm(ApiBaseModelWithIdNameLabelAndDesc):
  type: Code
  dataOriginDescription: str
  dataOriginType: Code
  populationIds: List[str] = []
