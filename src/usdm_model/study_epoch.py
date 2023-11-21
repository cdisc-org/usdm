from typing import Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class StudyEpoch(ApiBaseModelWithIdNameLabelAndDesc):
  type: Code
  previousId: Union[str, None] = None
  nextId: Union[str, None] = None
