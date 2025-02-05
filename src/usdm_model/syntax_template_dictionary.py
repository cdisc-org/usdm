from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc, ApiBaseModelWithId


class ParameterMap(ApiBaseModelWithId):
    tag: str
    reference: str
    instanceType: Literal["ParameterMap"]


class SyntaxTemplateDictionary(ApiBaseModelWithIdNameLabelAndDesc):
    parameterMaps: List[ParameterMap] = []  # Allow for empty list, not in API
    instanceType: Literal["SyntaxTemplateDictionary"]
