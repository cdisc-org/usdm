from typing import Literal, Union
from .api_base_model import ApiBaseModelWithId
from .code import Code
from .alias_code import AliasCode

class GeographicScope(ApiBaseModelWithId):
  type: Code
  code: Union[AliasCode, None] = None
  instanceType: Literal['GeographicScope'] = 'GeographicScope'

class SubjectEnrollment(GeographicScope):
  quantity: str
  instanceType: Literal['SubjectEnrollment'] = 'SubjectEnrollment'
