from .api_base_model import ApiBaseModelWithId
from .quantity import Quantity

class AdministrationDuration(ApiBaseModelWithId):
	quantity:	Quantity
	description: str
	durationWillVary: bool
	reasonDurationWillVary:	str
