from typing import List, Union
from .syntax_template import SyntaxTemplate
from .code import Code

class EligibilityCriteria(SyntaxTemplate):
  category: Code
  identifier: str
  nextCriterionId: Union[str, None] = None
  previousCriterionId: Union[str, None] = None