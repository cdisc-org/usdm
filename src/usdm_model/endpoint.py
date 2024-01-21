from .syntax_template import SyntaxTemplate
from .code import Code
from typing import Literal

class Endpoint(SyntaxTemplate):
  purpose: str
  level: Code
  instanceType: Literal['Endpoint']
