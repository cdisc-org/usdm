from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc

class Condition(ApiBaseModelWithIdNameLabelAndDesc):
  text: str
  dictionaryId: Union[str, None] = None
  contextIds: List[str] = []
  appliesToIds: List[str] = []
  instanceType: Literal['Condition']