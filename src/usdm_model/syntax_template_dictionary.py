from typing import Dict, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc

class SyntaxTemplateDictionary(ApiBaseModelWithIdNameLabelAndDesc):
  parameterMap: Dict
  instanceType: Literal['SyntaxTemplateDictionary']
