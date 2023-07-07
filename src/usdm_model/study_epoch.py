from typing import Union
from .api_base_model import ApiNameDescriptionModel
from .code import Code

class StudyEpoch(ApiNameDescriptionModel):
  studyEpochType: Code
  previousStudyEpochId: Union[str, None] = None
  nextStudyEpochId: Union[str, None] = None
