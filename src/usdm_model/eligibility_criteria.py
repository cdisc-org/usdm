from typing import List, Union
from .syntax_template import SyntaxTemplate
from .code import Code

class EligibilityCriteria(SyntaxTemplate):
  category: Code
  identifier: str
  nextId: Union[str, None] = None
  previousId: Union[str, None] = None