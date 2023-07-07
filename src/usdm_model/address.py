from .api_base_model import ApiIdModel
from .code import Code

class Address(ApiIdModel):
  text: str
  line: str
  city: str
  district: str
  state: str
  postalCode: str
  country: Code
