from typing import List, Union
from .api_base_model import ApiBaseModelWithIdAndName

class Content(ApiBaseModelWithIdAndName):
  sectionNumber: str
  sectionTitle: str
  text: Union[str, None] = None
  contentChildIds: List[str] = []