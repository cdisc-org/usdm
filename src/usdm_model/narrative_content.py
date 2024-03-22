from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdAndName

class NarrativeContent(ApiBaseModelWithIdAndName):
  sectionNumber: str
  sectionTitle: str
  text: Union[str, None] = None
  childIds: List[str] = []
  previousId: Union[str, None] = None
  nextId: Union[str, None] = None
  instanceType: Literal['NarrativeContent']
