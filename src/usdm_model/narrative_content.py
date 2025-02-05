from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdAndName


class NarrativeContentItem(ApiBaseModelWithIdAndName):
    text: str
    instanceType: Literal["NarrativeContentItem"]


class NarrativeContent(ApiBaseModelWithIdAndName):
    sectionNumber: Union[str, None] = None
    sectionTitle: Union[str, None] = None
    displaySectionNumber: bool
    displaySectionTitle: bool
    childIds: List[str] = []
    previousId: Union[str, None] = None
    nextId: Union[str, None] = None
    contentItemId: Union[str, None] = None
    instanceType: Literal["NarrativeContent"]
