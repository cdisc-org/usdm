from typing import Union, List, Literal
from .api_base_model import ApiBaseModelWithId


class PersonName(ApiBaseModelWithId):
    text: Union[str, None] = None
    familyName: Union[str, None] = None
    givenNames: List[str] = []
    prefixes: List[str] = []
    suffixes: List[str] = []
    instanceType: Literal["PersonName"]
