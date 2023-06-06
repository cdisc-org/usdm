from typing import Union
from .api_base_model import ApiBaseModel
from .code import Code

class Procedure(ApiBaseModel):
  procedureId: str
  procedureType: str
  procedureName: str
  procedureDescription: Union[str, None] = None
  procedureCode: Code
  procedureIsConditional: bool
  procedureIsConditionalReason: Union[str, None] = None
