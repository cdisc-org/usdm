from typing import List
from pydantic import NonNegativeInt
from .api_base_model import ApiNameDescriptionModel
from .code import Code

class StudyDesignPopulation(ApiNameDescriptionModel):
  plannedNumberOfParticipants: NonNegativeInt
  plannedMaximumAgeOfParticipants: str  
  plannedMinimumAgeOfParticipants: str
  plannedSexOfParticipants: List[Code] = []
