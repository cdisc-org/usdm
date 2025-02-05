from typing import List, Literal, Union
from .syntax_template import SyntaxTemplate
from .code import Code
from .endpoint import Endpoint


class Objective(SyntaxTemplate):
    level: Code
    endpoints: List[Endpoint] = []
    instanceType: Literal["Objective"]
