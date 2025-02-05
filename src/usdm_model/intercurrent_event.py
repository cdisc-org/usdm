from typing import Literal
from .syntax_template import SyntaxTemplate


class IntercurrentEvent(SyntaxTemplate):
    strategy: str
    instanceType: Literal["IntercurrentEvent"]
