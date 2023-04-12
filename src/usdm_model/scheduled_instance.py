from enum import Enum
from typing import List, Dict, Union, Literal

from .api_base_model import ApiBaseModel
from .timing import Timing

class ScheduledInstance(ApiBaseModel):
    scheduledInstanceId: str
    scheduledInstanceType: Literal['ACTIVITY', 'DECISION']
    scheduleSequenceNumber: int
    scheduleTimelineExitId: Union[str, None] = None
    scheduledInstanceEncounterId: Union[str, None] = None
    scheduledInstanceTimings: List[Timing] = []
    scheduledInstanceTimelineId: Union[str, None] = None

class ScheduledActivityInstance(ScheduledInstance):
    activityIds: List[str] = []

class ScheduledDecisionInstance(ScheduledInstance):
    conditionAssignments: List[List] = []