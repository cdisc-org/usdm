from typing import List, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .transition_rule import TransitionRule

class Encounter(ApiBaseModelWithIdNameLabelAndDesc):
  type: Union[Code, None] = None
  previousEncounterId: Union[str, None] = None
  nextEncounterId: Union[str, None] = None
  encounterScheduledAtTimingId: Union[str, None] = None
  encounterEnvironmentalSetting: Union[Code, None] = None
  encounterContactModes: List[Code] = []
  transitionStartRule: Union[TransitionRule, None] = None
  transitionEndRule: Union[TransitionRule, None] = None
