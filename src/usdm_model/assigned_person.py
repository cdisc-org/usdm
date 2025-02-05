from typing import Union, List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc


class AssignedPerson(ApiBaseModelWithIdNameLabelAndDesc):
    jobTitle: str
    organizationId: Union[str, None] = None
    instanceType: Literal["AssignedPerson"]
