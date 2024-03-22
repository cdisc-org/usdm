from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc, ApiBaseModelWithId

class ParameterMap(ApiBaseModelWithId):
  tag: str
  reference: str
  instanceType: Literal['ParameterMap']

class SyntaxTemplateDictionary(ApiBaseModelWithIdNameLabelAndDesc):
  parameterMaps: List[ParameterMap] = []
  instanceType: Literal['SyntaxTemplateDictionary']
