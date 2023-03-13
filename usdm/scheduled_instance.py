from enum import Enum
from typing import List, Dict

from .api_base_model import ApiBaseModel
from .timing import Timing

class ScheduledInstanceType(Enum):
  ACTIVITY = 1
  DECISION = 2

class ScheduledInstance(ApiBaseModel):
    scheduledInstanceId: str
    scheduledInstanceType: ScheduledInstanceType
    scheduleSequenceNumber: int
    scheduleTimelineExitId: str
    scheduledInstanceEncounterId: str
    scheduledInstanceTimings: List[Timing] = []
    scheduledInstanceTimelineId: str

class ScheduledActivityInstance(ScheduledInstance):
    activityIds: List[str] = []

class ScheduledDecisionInstance(ScheduledInstance):
    conditionAssignments: List[List] = []