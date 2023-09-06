from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class StudyArm(ApiBaseModelWithIdNameLabelAndDesc):
  type: Code
  studyArmDataOriginDescription: str
  dataOriginType: Code
