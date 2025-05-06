from typing import List, Union, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity_range import Quantity
from .duration import Duration
from .alias_code import AliasCode
from .comment_annotation import CommentAnnotation


class Administration(ApiBaseModelWithIdNameLabelAndDesc):
    duration: Duration
    dose: Union[Quantity, None] = None
    route: Union[AliasCode, None] = None
    frequency: Union[AliasCode, None] = None
    administrableProductId: Union[str, None] = None
    medicalDeviceId: Union[str, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["Administration"]
