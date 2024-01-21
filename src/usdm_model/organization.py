from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameAndLabel
from .code import Code
from .address import Address

class Organization(ApiBaseModelWithIdNameAndLabel):
  type: Code
  identifierScheme: str
  identifier: str
  legalAddress: Union[Address, None] = None
  instanceType: Literal['Organization'] = 'Organization'

class ResearchOrganization(Organization):
  manageIds: List[str]
  instanceType: Literal['ResearchOrganization']
