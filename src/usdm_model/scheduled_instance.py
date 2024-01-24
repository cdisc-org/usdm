from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithId

class ScheduledInstance(ApiBaseModelWithId):
  timelineId: Union[str, None] = None
  timelineExitId: Union[str, None] = None
  defaultConditionId: Union[str, None] = None
  epochId: Union[str, None] = None
  instanceType: Literal['ScheduledInstance']

class ScheduledActivityInstance(ScheduledInstance):
  activityIds: List[str] = []
  encounterId: Union[str, None] = None
  instanceType: Literal['ScheduledActivityInstance']

class ScheduledDecisionInstance(ScheduledInstance):
  conditionAssignments: List[List] = []
  instanceType: Literal['ScheduledDecisionInstance']
