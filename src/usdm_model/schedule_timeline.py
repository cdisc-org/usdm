from typing import List, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .schedule_timeline_exit import ScheduleTimelineExit
from .scheduled_instance import ScheduledInstance

class ScheduleTimeline(ApiBaseModelWithIdNameLabelAndDesc):
  mainTimeline: bool
  entryCondition: str
  scheduleTimelineEntryId: Union[str, None] = None
  scheduleTimelineExits: List[ScheduleTimelineExit] = []
  scheduleTimelineInstances: List[ScheduledInstance] = []