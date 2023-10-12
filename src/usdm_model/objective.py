from typing import List, Union
from .syntax_template import SyntaxTemplate
from .code import Code
from .endpoint import Endpoint

class Objective(SyntaxTemplate):
  level: Union[Code, None] = None
  objectiveEndpoints: List[Endpoint] = []