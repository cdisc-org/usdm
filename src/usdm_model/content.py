from typing import List, Union
from .api_base_model import ApiNameDescriptionModel

class Content(ApiNameDescriptionModel):
  sectionNumber: str
  sectionTitle: str
  text: Union[str, None] = None
  contentChildIds: List[str] = []