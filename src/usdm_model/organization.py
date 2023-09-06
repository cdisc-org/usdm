from typing import Union
from .api_base_model import ApiBaseModelWithIdAndName
from .code import Code
from .address import Address

class Organization(ApiBaseModelWithIdAndName):
  organizationIdentifierScheme: str
  organizationIdentifier: str
  organizationType: Code
  organizationLegalAddress: Union[Address, None] = None
