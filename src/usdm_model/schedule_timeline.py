from typing import List, Union
from .api_base_model import ApiNameDescriptionModel
from .schedule_timeline_exit import ScheduleTimelineExit
from .scheduled_instance import ScheduledInstance

class ScheduleTimeline(ApiNameDescriptionModel):
    mainTimeline: bool
    entryCondition: str
    scheduleTimelineEntryId: Union[str, None] = None
    scheduleTimelineExits: List[ScheduleTimelineExit] = []
    scheduleTimelineInstances: List[ScheduledInstance] = []