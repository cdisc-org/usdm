from typing import Union, List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .person_name import PersonName


class AssignedPerson(ApiBaseModelWithIdNameLabelAndDesc):
    personName: PersonName
    jobTitle: str
    organizationId: Union[str, None] = None
    instanceType: Literal["AssignedPerson"]
