from typing import Literal
from .api_base_model import ApiBaseModelWithId


class DocumentContentReference(ApiBaseModelWithId):
    sectionNumber: str
    sectionTitle: str
    appliesToId: str
    instanceType: Literal["DocumentContentReference"]
