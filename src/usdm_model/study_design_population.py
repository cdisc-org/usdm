from typing import List
from pydantic import NonNegativeInt
from .population_definition import PopulationDefinition
from .study_cohort import StudyCohort

class StudyDesignPopulation(PopulationDefinition):
  cohorts: List[StudyCohort] = []
