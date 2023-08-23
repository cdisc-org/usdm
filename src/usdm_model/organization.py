from typing import Union
from .api_base_model import ApiNameModel
from .code import Code
from .address import Address

class Organization(ApiNameModel):
  organizationIdentifierScheme: str
  organizationIdentifier: str
  organizationType: Code
  organizationLegalAddress: Union[Address, None] = None
