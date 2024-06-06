from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .comment_annotation import CommentAnnotation

class IntercurrentEvent(ApiBaseModelWithIdNameLabelAndDesc):
  strategy: str
  notes: List[CommentAnnotation] = []
  instanceType: Literal['IntercurrentEvent']
