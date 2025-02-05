from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameAndLabel
from .code import Code
from .address import Address
from .study_site import StudySite


class Organization(ApiBaseModelWithIdNameAndLabel):
    type: Code
    identifierScheme: str
    identifier: str
    legalAddress: Union[Address, None] = None
    managedSites: List[StudySite] = []
    instanceType: Literal["Organization"]
