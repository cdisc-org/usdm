from typing import Union
from .api_base_model import ApiBaseModel
from .code import Code
from .address import Address

class Organisation(ApiBaseModel):
  organizationId: str
  organisationIdentifierScheme: str
  organisationIdentifier: str
  organisationName: str
  organisationType: Code
  organizationLegalAddress: Union[Address, None] = None

  @classmethod
  def global_reuse(cls):
    return True

