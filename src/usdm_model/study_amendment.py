from typing import Union, List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .study_amendment_reason import StudyAmendmentReason
from .study_change import StudyChange
from .study_amendment_impact import StudyAmendmentImpact
from .geographic_scope import GeographicScope
from .subject_enrollment import SubjectEnrollment
from .governance_date import GovernanceDate
from .comment_annotation import CommentAnnotation


class StudyAmendment(ApiBaseModelWithIdNameLabelAndDesc):
    number: str
    summary: str
    primaryReason: StudyAmendmentReason
    secondaryReasons: List[StudyAmendmentReason] = []
    changes: List[StudyChange] = []  # Not in API
    impacts: List[StudyAmendmentImpact] = []
    geographicScopes: List[GeographicScope]
    enrollments: List[SubjectEnrollment] = []
    dateValues: List[GovernanceDate] = []
    previousId: Union[str, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["StudyAmendment"]
