from typing import List
from .alias_code import AliasCode
from .api_base_model import ApiNameModel
from .response_code import ResponseCode

class BiomedicalConceptProperty(ApiNameModel):
  bcPropertyRequired: bool
  bcPropertyEnabled: bool
  bcPropertyDatatype: str
  bcPropertyResponseCodes: List[ResponseCode] = []
  bcPropertyConceptCode: AliasCode
