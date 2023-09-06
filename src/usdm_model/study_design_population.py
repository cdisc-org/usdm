from typing import List
from pydantic import NonNegativeInt
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class StudyDesignPopulation(ApiBaseModelWithIdNameLabelAndDesc):
  plannedNumberOfParticipants: NonNegativeInt
  plannedMaximumAgeOfParticipants: str  
  plannedMinimumAgeOfParticipants: str
  plannedSexOfParticipants: List[Code] = []
