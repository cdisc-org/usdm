from typing import List
from .api_base_model import ApiBaseModelWithId

class StudyCell(ApiBaseModelWithId):
  studyArmId: str
  studyEpochId: str
  studyElementIds: List[str] = []
