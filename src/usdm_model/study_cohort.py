from typing import List
from pydantic import NonNegativeInt
from .population_definition import PopulationDefinition
from .characteristic import Characteristic

class StudyCohort(PopulationDefinition):
  characteristics: List[Characteristic] = []
