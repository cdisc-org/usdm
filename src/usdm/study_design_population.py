from .api_base_model import ApiBaseModel
from typing import List
from .code import Code

class StudyDesignPopulation(ApiBaseModel):
  studyDesignPopulationId: str
  populationDescription: str
  plannedNumberOfParticipants: int
  plannedMaximumAgeOfParticipants: str  
  plannedMinimumAgeOfParticipants: str
  plannedSexOfParticipants: List[Code] = []
