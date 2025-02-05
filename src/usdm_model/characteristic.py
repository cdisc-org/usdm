from typing import Literal
from .syntax_template import SyntaxTemplate


class Characteristic(SyntaxTemplate):
    instanceType: Literal["Characteristic"]
