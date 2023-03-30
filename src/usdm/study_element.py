from typing import Union
from .api_base_model import ApiBaseModel
from .transition_rule import TransitionRule

from uuid import UUID

class StudyElement(ApiBaseModel):
  studyElementId: str
  studyElementName: str
  studyElementDescription: str
  transitionStartRule: Union[TransitionRule, None] = None
  transitionEndRule: Union[TransitionRule, None] = None
