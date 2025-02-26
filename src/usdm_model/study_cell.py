from typing import List, Literal
from .api_base_model import ApiBaseModelWithId


class StudyCell(ApiBaseModelWithId):
    armId: str
    epochId: str
    elementIds: List[str]
    instanceType: Literal["StudyCell"]
