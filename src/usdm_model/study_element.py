from typing import Union
from .api_base_model import ApiNameDescriptionModel
from .transition_rule import TransitionRule

class StudyElement(ApiNameDescriptionModel):
  transitionStartRule: Union[TransitionRule, None] = None
  transitionEndRule: Union[TransitionRule, None] = None
