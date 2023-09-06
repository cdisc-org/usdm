from typing import Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class StudyEpoch(ApiBaseModelWithIdNameLabelAndDesc):
  type: Code
  previousStudyEpochId: Union[str, None] = None
  nextStudyEpochId: Union[str, None] = None
