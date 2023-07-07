from typing import List
from pydantic import NonNegativeInt
from .api_base_model import ApiIdModel
from .code import Code

class StudyDesignPopulation(ApiIdModel):
  populationDescription: str
  plannedNumberOfParticipants: NonNegativeInt
  plannedMaximumAgeOfParticipants: str  
  plannedMinimumAgeOfParticipants: str
  plannedSexOfParticipants: List[Code] = []
