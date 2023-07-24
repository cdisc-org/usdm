from typing import List
from pydantic import NonNegativeInt
from .api_base_model import ApiDescriptionModel
from .code import Code

class StudyDesignPopulation(ApiDescriptionModel):
  plannedNumberOfParticipants: NonNegativeInt
  plannedMaximumAgeOfParticipants: str  
  plannedMinimumAgeOfParticipants: str
  plannedSexOfParticipants: List[Code] = []
