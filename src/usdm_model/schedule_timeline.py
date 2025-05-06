from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .schedule_timeline_exit import ScheduleTimelineExit
from .scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
from .timing import Timing
from .duration import Duration


class ScheduleTimeline(ApiBaseModelWithIdNameLabelAndDesc):
    mainTimeline: bool
    entryCondition: str
    entryId: str
    exits: List[ScheduleTimelineExit] = []
    timings: List[Timing] = []
    instances: List[Union[ScheduledActivityInstance, ScheduledDecisionInstance]] = []
    plannedDuration: Union[Duration, None] = None
    instanceType: Literal["ScheduleTimeline"]
