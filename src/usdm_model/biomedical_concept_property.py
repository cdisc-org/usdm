from typing import List
from .alias_code import AliasCode
from .api_base_model import ApiBaseModelWithIdNameAndLabel
from .response_code import ResponseCode

class BiomedicalConceptProperty(ApiBaseModelWithIdNameAndLabel):
  bcPropertyRequired: bool
  bcPropertyEnabled: bool
  bcPropertyDatatype: str
  bcPropertyResponseCodes: List[ResponseCode] = []
  code: AliasCode
