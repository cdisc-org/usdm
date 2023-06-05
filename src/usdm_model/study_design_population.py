from pydantic import NonNegativeInt
from typing import List
from .api_base_model import ApiBaseModel
from .code import Code

class StudyDesignPopulation(ApiBaseModel):
  studyDesignPopulationId: str
  populationDescription: str
  plannedNumberOfParticipants: NonNegativeInt
  plannedMaximumAgeOfParticipants: str  
  plannedMinimumAgeOfParticipants: str
  plannedSexOfParticipants: List[Code] = []
