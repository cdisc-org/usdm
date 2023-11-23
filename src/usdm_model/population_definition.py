from typing import List, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code
from .range import Range
from .quantity import Quantity
from .eligibility_criteria import EligibilityCriteria

class PopulationDefinition(ApiBaseModelWithIdNameLabelAndDesc):
  plannedEnrollmentNumber: Union[Range, None] = None
  plannedCompletionNumber: Union[Range, None] = None
  plannedMaximumAge: Union[Quantity, None] = None
  plannedMinimumAge: Union[Quantity, None] = None
  plannedSex: List[Code] = []
  criteria: List[EligibilityCriteria] = []
