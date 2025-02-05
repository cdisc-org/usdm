from typing import List, Union, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .administration_duration import AdministrationDuration
from .alias_code import AliasCode
from .comment_annotation import CommentAnnotation


class Administration(ApiBaseModelWithIdNameLabelAndDesc):
    duration: AdministrationDuration
    dose: Quantity
    route: AliasCode
    frequency: AliasCode
    administrableProductId: Union[str, None] = None
    medicalDeviceId: Union[str, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["Administration"]
