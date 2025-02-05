from typing import Literal, Union
from .syntax_template import SyntaxTemplate
from .code import Code


class EligibilityCriterion(SyntaxTemplate):
    category: Code
    identifier: str
    nextId: Union[str, None] = None
    previousId: Union[str, None] = None
    instanceType: Literal["EligibilityCriterion"]
