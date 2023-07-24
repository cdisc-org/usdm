from .api_base_model import ApiNameDescriptionModel
from .code import Code

class StudyArm(ApiNameDescriptionModel):
  studyArmType: Code
  studyArmDataOriginDescription: str
  studyArmDataOriginType: Code
