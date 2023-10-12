from typing import Union
from .api_base_model import ApiBaseModelWithId
from .study_amendment_reason import StudyAmendmentReason
from .enrollment import Enrollment

class StudyAmendment(ApiBaseModelWithId):
  number: str
  summary: str
  substantialImpact: bool
  primaryReason: StudyAmendmentReason
  secondaryReason: Union[StudyAmendmentReason, None] = None
  enrollment: Enrollment
  previousId: Union[str, None] = None
