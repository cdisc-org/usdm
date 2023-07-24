from typing import List, Dict, Union, Literal
from .api_base_model import ApiIdModel
from .timing import Timing

class ScheduledInstance(ApiIdModel):
  scheduledInstanceType: Literal['ACTIVITY', 'DECISION']
  scheduleTimelineExitId: Union[str, None] = None
  scheduledInstanceTimings: List[Timing] = []
  scheduledInstanceTimelineId: Union[str, None] = None
  defaultConditionId: Union[str, None] = None
  epochId: Union[str, None] = None

class ScheduledActivityInstance(ScheduledInstance):
  activityIds: List[str] = []
  scheduledActivityInstanceEncounterId: Union[str, None] = None

class ScheduledDecisionInstance(ScheduledInstance):
  conditionAssignments: List[List] = []