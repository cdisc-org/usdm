from typing import List
from .api_base_model import ApiIdModel

class StudyCell(ApiIdModel):
  studyArmId: str
  studyEpochId: str
  studyElementIds: List[str] = []
