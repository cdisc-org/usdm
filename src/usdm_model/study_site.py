from typing import Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .geographic_scope import SubjectEnrollment

class StudySite(ApiBaseModelWithIdNameLabelAndDesc):
  currentEnrollment: Union[SubjectEnrollment, None] = None
  instanceType: Literal['StudySite'] = 'StudySite'
