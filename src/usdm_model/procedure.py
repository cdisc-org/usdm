from .api_base_model import ApiBaseModel
from .code import Code

class Procedure(ApiBaseModel):
  procedureId: str
  procedureType: str
  procedureName: str
  procedureDescription: str
  procedureCode: Code
  procedureIsConditional: bool
  procedureIsConditionalReason: str
