from typing import List
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from datetime import date
from .code import Code
from .geographic_scope import GeographicScope

class GovernanceDate(ApiBaseModelWithIdNameLabelAndDesc):
  type: Code
  dataValue: date
  geographicScopes: List[GeographicScope]
