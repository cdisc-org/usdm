from typing import Literal, Union
from .api_base_model import ApiBaseModelWithId
from .code import Code
from .alias_code import AliasCode
from .quantity import Quantity
from .study_site import StudySite

class GeographicScope(ApiBaseModelWithId):
  type: Code
  code: Union[AliasCode, None] = None
  instanceType: Literal['GeographicScope']

class SubjectEnrollment(GeographicScope):
  quantity: Quantity
  appliesTo: Union[StudySite, None] = None
  instanceType: Literal['SubjectEnrollment']
