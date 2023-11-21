from typing import List
from .api_base_model import ApiBaseModelWithId

class StudyCell(ApiBaseModelWithId):
  armId: str
  epochId: str
  elementIds: List[str] = []
