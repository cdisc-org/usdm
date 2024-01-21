from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .agent_administration import AgentAdministration
from .code import Code

class StudyIntervention(ApiBaseModelWithIdNameLabelAndDesc):
  role:	Code
  type:	Code
  minimumResponseDuration: Quantity
  codes: List[Code] = []
  administrations: List[AgentAdministration]
  productDesignation:	Code
  pharmacologicClass:	Code
  instanceType: Literal['StudyIntervention']