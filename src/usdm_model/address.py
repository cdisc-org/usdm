from typing import Union
from .api_base_model import ApiBaseModelWithId
from .code import Code

class Address(ApiBaseModelWithId):
  text: str = ""
  line: str = ""
  city: str = ""
  district: str = ""
  state: str = ""
  postalCode: str = ""
  country: Union[Code, None] = None
