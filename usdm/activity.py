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
  biomedicalConcepts: List[str] = []
  bcCategories: List[str] = []
  bcSurrogates: List[str] = []
  activityTimelineId: str
