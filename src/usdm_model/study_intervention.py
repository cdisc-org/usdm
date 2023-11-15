from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .quantity import Quantity
from .agent_administration import AgentAdministration
from .code import Code

class StudyIntervention(ApiBaseModelWithIdNameLabelAndDesc):
  role:	Code
  type:	Code
  minimumResponseDuration: Quantity
  codes:	Code
  administrations: AgentAdministration
  productDesignation:	Code
  pharmacologicClass:	Code
