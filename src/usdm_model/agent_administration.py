from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .administration_duration import AdministrationDuration
from .code import Code
from typing import Literal

class AgentAdministration(ApiBaseModelWithIdNameLabelAndDesc):
  duration:	AdministrationDuration
  dose:	Quantity
  route:	Code
  frequency:	Code
  instanceType: Literal['AgentAdministration']
