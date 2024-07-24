from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .administration_duration import AdministrationDuration
from .alias_code import AliasCode
from .comment_annotation import CommentAnnotation

class AgentAdministration(ApiBaseModelWithIdNameLabelAndDesc):
  duration:	AdministrationDuration
  dose:	Quantity
  route:	AliasCode
  frequency:	AliasCode
  notes: List[CommentAnnotation] = []
  instanceType: Literal['AgentAdministration']
