from typing import Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class Procedure(ApiBaseModelWithIdNameLabelAndDesc):
  procedureType: str
  code: Code
  procedureIsConditional: bool
  procedureIsConditionalReason: Union[str, None] = None
