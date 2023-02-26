from typing import Union
from .api_base_model import ApiBaseModel
from .code import Code
from uuid import UUID

class StudyArm(ApiBaseModel):
  studyArmId: str
  studyArmName: str
  studyArmDescription: str
  studyArmType: str
  studyArmDataOriginDescription: str
  studyArmDataOriginType: Code
