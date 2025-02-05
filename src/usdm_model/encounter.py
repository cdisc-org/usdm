from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .comment_annotation import CommentAnnotation
from .transition_rule import TransitionRule


class Encounter(ApiBaseModelWithIdNameLabelAndDesc):
    type: Code
    previousId: Union[str, None] = None
    nextId: Union[str, None] = None
    scheduledAtId: Union[str, None] = None
    environmentalSettings: List[Code] = []
    contactModes: List[Code] = []
    transitionStartRule: Union[TransitionRule, None] = None
    transitionEndRule: Union[TransitionRule, None] = None
    notes: List[CommentAnnotation] = []
    instanceType: Literal["Encounter"]
