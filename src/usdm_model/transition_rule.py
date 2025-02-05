from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from typing import Literal


class TransitionRule(ApiBaseModelWithIdNameLabelAndDesc):
    text: str
    instanceType: Literal["TransitionRule"]
