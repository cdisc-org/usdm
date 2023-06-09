from typing import Union
from .api_base_model import ApiBaseModel
from .transition_rule import TransitionRule

class StudyElement(ApiBaseModel):
  studyElementId: str
  studyElementName: str
  studyElementDescription: Union[str, None] = None
  transitionStartRule: Union[TransitionRule, None] = None
  transitionEndRule: Union[TransitionRule, None] = None
