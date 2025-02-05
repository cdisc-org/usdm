from typing import List, Literal
from .syntax_template import SyntaxTemplate


class Condition(SyntaxTemplate):
    contextIds: List[str] = []
    appliesToIds: List[str] = []
    instanceType: Literal["Condition"]
