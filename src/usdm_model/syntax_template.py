from typing import Union, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc

class SyntaxTemplate(ApiBaseModelWithIdNameLabelAndDesc):
  text: str
  dictionaryId: Union[str, None] = None
  instanceType: Literal['SyntaxTemplate']
