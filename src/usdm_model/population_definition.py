from typing import List
from pydantic import NonNegativeInt
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .range import Range
from .quantity import Quantity
from .eligibility_criteria import EligibilityCriteria

class PopulationDefinition(ApiBaseModelWithIdNameLabelAndDesc):
  plannedEnrollmentNumber: Range
  plannedCompletionNumber: Range
  plannedMaximumAge: Quantity  
  plannedMinimumAge: Quantity
  plannedSex: List[Code] = []
  criteria: List[EligibilityCriteria]
