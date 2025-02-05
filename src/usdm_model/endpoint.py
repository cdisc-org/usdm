from typing import Literal
from .syntax_template import SyntaxTemplate
from .code import Code


class Endpoint(SyntaxTemplate):
    purpose: str
    level: Code
    instanceType: Literal["Endpoint"]
