from typing import Union, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .syntax_template_dictionary import SyntaxTemplateDictionary

class SyntaxTemplate(ApiBaseModelWithIdNameLabelAndDesc):
  instanceType: Literal['ENDPOINT', 'OBJECTIVE', 'ELIGIBILITY_CRITERIA']
  text: str
  dictionaryId: Union[str, None] = None
