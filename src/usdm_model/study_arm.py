from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class StudyArm(ApiBaseModelWithIdNameLabelAndDesc):
  studyArmType: Code
  studyArmDataOriginDescription: str
  studyArmDataOriginType: Code
