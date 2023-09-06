from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .syntax_template_dictionary import SyntaxTemplateDictionary

class SyntaxTemplate(ApiBaseModelWithIdNameLabelAndDesc):
  text: str = None
  dictionary: SyntaxTemplateDictionary
