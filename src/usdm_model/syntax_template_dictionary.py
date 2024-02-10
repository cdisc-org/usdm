from typing import Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc

class SyntaxTemplateDictionary(ApiBaseModelWithIdNameLabelAndDesc):
  parameterMap: dict
  instanceType: Literal['SyntaxTemplateDictionary']
