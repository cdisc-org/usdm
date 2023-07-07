from typing import List
from .api_base_model import ApiBaseModel

class StudyCell(ApiBaseModel):
  studyArmId: str
  studyEpochId: str
  studyElementIds: List[str] = []
