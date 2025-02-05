from typing import Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code


class StudySite(ApiBaseModelWithIdNameLabelAndDesc):
    country: Code
    instanceType: Literal["StudySite"]
