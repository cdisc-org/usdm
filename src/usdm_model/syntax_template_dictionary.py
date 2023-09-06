from typing import Dict
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc

class SyntaxTemplateDictionary(ApiBaseModelWithIdNameLabelAndDesc):
  text: str = None
  parameterMap: Dict