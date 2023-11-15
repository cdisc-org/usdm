from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .administration_duration import AdministrationDuration
from .code import Code

class AgentAdministration(ApiBaseModelWithIdNameLabelAndDesc):
	duration:	AdministrationDuration
	dose:	Quantity
	route:	Code
	frequency:	Code
