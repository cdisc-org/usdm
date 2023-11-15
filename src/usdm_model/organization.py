from typing import Union
from .api_base_model import ApiBaseModelWithIdNameAndLabel
from .code import Code
from .address import Address

class Organization(ApiBaseModelWithIdNameAndLabel):
  type: Code
  identifierScheme: str
  identifier: str
  legalAddress: Union[Address, None] = None
