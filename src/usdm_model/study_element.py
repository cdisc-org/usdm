from typing import Union, List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .transition_rule import TransitionRule

class StudyElement(ApiBaseModelWithIdNameLabelAndDesc):
  transitionStartRule: Union[TransitionRule, None] = None
  transitionEndRule: Union[TransitionRule, None] = None
  studyInterventionIds: List[str] = []
  instanceType: Literal['StudyElement']
