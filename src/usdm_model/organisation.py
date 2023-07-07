from typing import Union
from .api_base_model import ApiIdModel
from .code import Code
from .address import Address

class Organisation(ApiIdModel):
  organisationIdentifierScheme: str
  organisationIdentifier: str
  organisationName: str
  organisationType: Code
  organizationLegalAddress: Union[Address, None] = None
