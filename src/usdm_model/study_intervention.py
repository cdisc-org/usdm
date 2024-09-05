from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .administration import Administration
from .code import Code
from .comment_annotation import CommentAnnotation

class StudyIntervention(ApiBaseModelWithIdNameLabelAndDesc):
  role:	Code
  type:	Code
  minimumResponseDuration: Union[Quantity, None] = None
  codes: List[Code] = []
  administrations: List[Administration] = []
  productDesignation:	Code
  notes: List[CommentAnnotation] = []
  instanceType: Literal['StudyIntervention']
