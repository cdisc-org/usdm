from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .schedule_timeline_exit import ScheduleTimelineExit
from .scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance

class ScheduleTimeline(ApiBaseModelWithIdNameLabelAndDesc):
  mainTimeline: bool
  entryCondition: str
  entryId: str
  exits: List[ScheduleTimelineExit] = []
  instances: List[Union[ScheduledActivityInstance, ScheduledDecisionInstance]] = []
  instanceType: Literal['ScheduleTimeline'] = 'ScheduleTimeline'
