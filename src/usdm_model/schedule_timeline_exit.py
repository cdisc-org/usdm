from .api_base_model import ApiBaseModelWithId
from typing import Literal


class ScheduleTimelineExit(ApiBaseModelWithId):
    instanceType: Literal["ScheduleTimelineExit"]
