from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc, ApiBaseModelWithId


class ConditionAssignment(ApiBaseModelWithId):
    condition: str
    conditionTargetId: str
    instanceType: Literal["ConditionAssignment"]


class ScheduledInstance(ApiBaseModelWithIdNameLabelAndDesc):
    defaultConditionId: Union[str, None] = None
    epochId: Union[str, None] = None
    instanceType: Literal["ScheduledInstance"]


class ScheduledActivityInstance(ScheduledInstance):
    timelineId: Union[str, None] = None
    timelineExitId: Union[str, None] = None
    activityIds: List[str] = []
    encounterId: Union[str, None] = None
    instanceType: Literal["ScheduledActivityInstance"]


class ScheduledDecisionInstance(ScheduledInstance):
    conditionAssignments: List[
        ConditionAssignment
    ] = []  # Allow for empty list, not in API
    instanceType: Literal["ScheduledDecisionInstance"]
