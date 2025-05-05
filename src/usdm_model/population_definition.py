from typing import Union, List, Literal, Annotated
from annotated_types import Len
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .quantity_range import Quantity, Range
from .characteristic import Characteristic
from .comment_annotation import CommentAnnotation


class PopulationDefinition(ApiBaseModelWithIdNameLabelAndDesc):
    includesHealthySubjects: bool
    plannedEnrollmentNumber: Union[Quantity, Range, None] = None
    plannedCompletionNumber: Union[Quantity, Range, None] = None
    plannedSex: Annotated[List[Code], Len(min_length=0, max_length=2)] = []
    criterionIds: List[str] = []
    plannedAge: Union[Range, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["PopulationDefinition"]


class StudyCohort(PopulationDefinition):
    characteristics: List[Characteristic] = []
    indicationIds: List[str] = []
    instanceType: Literal["StudyCohort"]


class StudyDesignPopulation(PopulationDefinition):
    cohorts: List[StudyCohort] = []
    instanceType: Literal["StudyDesignPopulation"]
