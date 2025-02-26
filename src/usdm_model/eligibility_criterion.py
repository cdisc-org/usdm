from typing import Literal, Union, List
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .syntax_template import SyntaxTemplate
from .comment_annotation import CommentAnnotation
from .code import Code


class EligibilityCriterion(ApiBaseModelWithIdNameLabelAndDesc):
    category: Code
    identifier: str
    criterionItemId: str
    nextId: Union[str, None] = None
    previousId: Union[str, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["EligibilityCriterion"]


class EligibilityCriterionItem(SyntaxTemplate):
    instanceType: Literal["EligibilityCriterionItem"]
