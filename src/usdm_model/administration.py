from typing import List, Union, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .administration_duration import AdministrationDuration
from .administrable_product import AdministrableProduct
from .alias_code import AliasCode
from .comment_annotation import CommentAnnotation

class Administration(ApiBaseModelWithIdNameLabelAndDesc):
  duration:	AdministrationDuration
  dose:	Quantity
  route: AliasCode
  frequency: AliasCode
  administrableProduct: Union[AdministrableProduct, None] = None
  notes: List[CommentAnnotation] = []
  instanceType: Literal['AgentAdministration']
