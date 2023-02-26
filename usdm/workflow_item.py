from typing import Union
from .api_base_model import ApiBaseModel

class WorkflowItem(ApiBaseModel):
  workflowItemId: str
  workflowItemDescription: str
  previousWorkflowItemId: Union[str, None] = None
  nextWorkflowItemId: Union[str, None] = None
  workflowItemEncounterId: Union[str, None] = None
  workflowItemActivityId: Union[str, None] = None