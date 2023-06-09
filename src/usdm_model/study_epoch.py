from typing import Union
from .api_base_model import ApiBaseModel
from .code import Code

class StudyEpoch(ApiBaseModel):
  studyEpochId: str
  studyEpochName: str
  studyEpochDescription: Union[str, None] = None
  studyEpochType: Code
  previousStudyEpochId: Union[str, None] = None
  nextStudyEpochId: Union[str, None] = None
