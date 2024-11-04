from typing import Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .geographic_scope import GeographicScope

class SubjectEnrollment(ApiBaseModelWithIdNameLabelAndDesc):
  quantity: Quantity
  appliesTo: Union[GeographicScope, None] = None
  appliesToId: Union[str, None] = None
  instanceType: Literal['SubjectEnrollment']
