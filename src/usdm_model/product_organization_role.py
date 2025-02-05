from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code


class ProductOrganizationRole(ApiBaseModelWithIdNameLabelAndDesc):
    code: Code
    appliesToIds: List[str] = []
    organizationId: str
    instanceType: Literal["ProductOrganizationRole"]
