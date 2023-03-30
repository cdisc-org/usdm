from typing import List, Union
from .api_base_model import ApiBaseModel
from .code import Code
from .encounter import Encounter

from uuid import UUID

class StudyEpoch(ApiBaseModel):
  studyEpochId: str
  studyEpochName: str
  studyEpochDescription: str
  studyEpochType: Code
  previousStudyEpochId: Union[str, None] = None
  nextStudyEpochId: Union[str, None] = None
  encounterIds: List[str] = []
