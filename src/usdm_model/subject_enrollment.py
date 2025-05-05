from typing import Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity_range import Quantity
from .geographic_scope import GeographicScope


class SubjectEnrollment(ApiBaseModelWithIdNameLabelAndDesc):
    quantity: Quantity
    forGeographicScope: Union[GeographicScope, None] = None
    forStudyCohortId: Union[str, None] = None
    forStudySiteId: Union[str, None] = None
    instanceType: Literal["SubjectEnrollment"]
