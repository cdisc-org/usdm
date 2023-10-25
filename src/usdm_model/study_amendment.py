from typing import Union, List
from .api_base_model import ApiBaseModelWithId
from .study_amendment_reason import StudyAmendmentReason
from .subject_enrollment import SubjectEnrollment

class StudyAmendment(ApiBaseModelWithId):
  number: str
  summary: str
  substantialImpact: bool
  primaryReason: StudyAmendmentReason
  secondaryReasons: List[StudyAmendmentReason] = []
  enrollments: List[SubjectEnrollment]
  previousId: Union[str, None] = None
