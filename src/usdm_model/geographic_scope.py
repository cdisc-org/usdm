from typing import Literal
from .api_base_model import ApiBaseModelWithId
from .code import Code
from .alias_code import AliasCode

class GeographicScope(ApiBaseModelWithId):
  instanceType: Literal['GEOGRAPHIC_SCOPE', 'SUBJECT_ENROLLMENT']
  type: Code
  code: AliasCode
