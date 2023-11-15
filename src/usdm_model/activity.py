from typing import List, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .procedure import Procedure

class Activity(ApiBaseModelWithIdNameLabelAndDesc):
  previousId: Union[str, None] = None
  nextId: Union[str, None] = None
  definedProcedures: List[Procedure] = []
  isConditional: bool
  isConditionalReason: Union[str, None] = None
  biomedicalConceptIds: List[str] = []
  bcCategoryIds: List[str] = []
  bcSurrogateIds: List[str] = []
  timelineId: Union[str, None] = None
