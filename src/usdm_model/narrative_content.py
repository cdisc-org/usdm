from typing import List, Union
from .api_base_model import ApiBaseModelWithIdAndName

class NarrativeContent(ApiBaseModelWithIdAndName):
  sectionNumber: str
  sectionTitle: str
  text: Union[str, None] = None
  childrenIds: List[str] = []
