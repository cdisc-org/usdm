from typing import Union, List
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .transition_rule import TransitionRule
from .study_intervention import StudyIntervention

class StudyElement(ApiBaseModelWithIdNameLabelAndDesc):
  transitionStartRule: Union[TransitionRule, None] = None
  transitionEndRule: Union[TransitionRule, None] = None
  studyInterventionIds: List[str] = []
