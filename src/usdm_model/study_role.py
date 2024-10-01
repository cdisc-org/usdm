from typing import Union, List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .masking import Masking
from .assigned_person import AssignedPerson

class StudyRole(ApiBaseModelWithIdNameLabelAndDesc):
  code: Code
  appliesToIds: List[str] = []  # Going to allow for an mpty list but really a role 
                                # should be attached to a Study Version or Design
  assignedPersons: List[AssignedPerson] = []
  organizationIds: List[str] = []
  masking: Union[Masking, None] = None
  instanceType: Literal['StudyRole']
