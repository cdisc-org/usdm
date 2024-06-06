from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .agent_administration import AgentAdministration
from .code import Code
from .comment_annotation import CommentAnnotation

class StudyIntervention(ApiBaseModelWithIdNameLabelAndDesc):
  role:	Code
  type:	Code
  minimumResponseDuration: Union[Quantity, None] = None
  codes: List[Code] = []
  administrations: List[AgentAdministration] = []
  productDesignation:	Code
  pharmacologicClass:	Union[Code, None] = None
  notes: List[CommentAnnotation] = []
  instanceType: Literal['StudyIntervention']
