from typing import List, Union
from .api_base_model import ApiNameDescriptionModel
from .procedure import Procedure

class Activity(ApiNameDescriptionModel):
  previousActivityId: Union[str, None] = None
  nextActivityId: Union[str, None] = None
  definedProcedures: List[Procedure] = []
  activityIsConditional: bool
  activityIsConditionalReason: Union[str, None] = None
  biomedicalConceptIds: List[str] = []
  bcCategoryIds: List[str] = []
  bcSurrogateIds: List[str] = []
  activityTimelineId: Union[str, None] = None
