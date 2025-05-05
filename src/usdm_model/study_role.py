from typing import Union, List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .masking import Masking
from .assigned_person import AssignedPerson
from .comment_annotation import CommentAnnotation


class StudyRole(ApiBaseModelWithIdNameLabelAndDesc):
    code: Code
    appliesToIds: List[str] = []  # Going to allow for an empty list but really a role
    # should be attached to a Study Version or Design
    assignedPersons: List[AssignedPerson] = []
    organizationIds: List[str] = []
    masking: Union[Masking, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["StudyRole"]
