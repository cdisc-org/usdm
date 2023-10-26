from typing import Union
from .api_base_model import ApiBaseModelWithId
from .code import Code

class StudyAmendmentReason(ApiBaseModelWithId):
  code: Code
  otherReason: Union[str, None] = None
