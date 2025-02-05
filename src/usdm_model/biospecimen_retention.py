from typing import Union, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc


class BiospecimenRetention(ApiBaseModelWithIdNameLabelAndDesc):
    isRetained: bool
    includesDNA: Union[bool, None] = None
    instanceType: Literal["BiospecimenRetention"]
