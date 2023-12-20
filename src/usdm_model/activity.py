from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .procedure import Procedure

class Activity(ApiBaseModelWithIdNameLabelAndDesc):
  previousId: Union[str, None] = None
  nextId: Union[str, None] = None
  definedProcedures: List[Procedure] = []
  biomedicalConceptIds: List[str] = []
  bcCategoryIds: List[str] = []
  bcSurrogateIds: List[str] = []
  timelineId: Union[str, None] = None
  instanceType: Literal['Activity'] = 'Activity'
