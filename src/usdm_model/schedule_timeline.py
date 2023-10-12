from typing import List, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .schedule_timeline_exit import ScheduleTimelineExit
from .scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance

class ScheduleTimeline(ApiBaseModelWithIdNameLabelAndDesc):
  mainTimeline: bool
  entryCondition: str
  scheduleTimelineEntryId: str
  scheduleTimelineExits: List[ScheduleTimelineExit] = []
  scheduleTimelineInstances: List[Union[ScheduledActivityInstance, ScheduledDecisionInstance]] = []
