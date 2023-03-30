from typing import List
from .alias_code import AliasCode
from .api_base_model import ApiBaseModel
from .response_code import ResponseCode

class BiomedicalConceptProperty(ApiBaseModel):
  bcPropertyId: str
  bcPropertyName: str
  bcPropertyRequired: bool
  bcPropertyEnabled: bool
  bcPropertyDatatype: str
  bcPropertyResponseCodes: List[ResponseCode] = []
  bcPropertyConceptCode: AliasCode
