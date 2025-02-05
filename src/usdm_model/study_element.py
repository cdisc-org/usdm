from typing import Union, List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .transition_rule import TransitionRule
from .comment_annotation import CommentAnnotation


class StudyElement(ApiBaseModelWithIdNameLabelAndDesc):
    transitionStartRule: Union[TransitionRule, None] = None
    transitionEndRule: Union[TransitionRule, None] = None
    studyInterventionIds: List[str] = []
    notes: List[CommentAnnotation] = []
    instanceType: Literal["StudyElement"]
