from typing import List, Dict, Union, Literal
from .api_base_model import ApiBaseModelWithId
from .timing import Timing

class ScheduledInstance(ApiBaseModelWithId):
  instanceType: Literal['ACTIVITY', 'DECISION']
  timings: List[Timing] = []
  timelineId: Union[str, None] = None
  timelineExitId: Union[str, None] = None
  defaultConditionId: Union[str, None] = None
  epochId: Union[str, None] = None

class ScheduledActivityInstance(ScheduledInstance):
  activityIds: List[str] = []
  encounterId: Union[str, None] = None

class ScheduledDecisionInstance(ScheduledInstance):
  conditionAssignments: List[List] = []
