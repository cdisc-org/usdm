from typing import List, Union
from .api_base_model import ApiBaseModel
from .procedure import Procedure

class Activity(ApiBaseModel):
  activityId: str
  activityName: str
  activityDescription: str
  previousActivityId: Union[str, None] = None
  nextActivityId: Union[str, None] = None
  definedProcedures: List[Procedure] = []
  activityIsConditional: bool
  activityIsConditionalReason: str
  biomedicalConceptIds: List[str] = []
  bcCategoryIds: List[str] = []
  bcSurrogateIds: List[str] = []
  activityTimelineId: str
