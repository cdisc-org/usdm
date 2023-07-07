from .api_base_model import ApiBaseModel
from .code import Code

class Address(ApiBaseModel):
  text: str
  line: str
  city: str
  district: str
  state: str
  postalCode: str
  country: Code
