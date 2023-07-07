from typing import Union
from .api_base_model import ApiNameDescriptionModel
from .code import Code

class Procedure(ApiNameDescriptionModel):
  procedureType: str
  procedureCode: Code
  procedureIsConditional: bool
  procedureIsConditionalReason: Union[str, None] = None
