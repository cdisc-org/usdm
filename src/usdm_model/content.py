from typing import List, Union
from .api_base_model import ApiNameModel

class Content(ApiNameModel):
  sectionNumber: str
  sectionTitle: str
  text: Union[str, None] = None
  contentChildIds: List[str] = []