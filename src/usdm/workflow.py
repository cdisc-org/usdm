from typing import List, Union
from .api_base_model import ApiBaseModel
from .workflow_item import WorkflowItem
from uuid import UUID

class Workflow(ApiBaseModel):
  workflowId: str
  workflowDescription: str
  workflowItems: List[WorkflowItem] = []