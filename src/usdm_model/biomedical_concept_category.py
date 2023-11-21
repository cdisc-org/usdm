from typing import List, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .alias_code import AliasCode

class BiomedicalConceptCategory(ApiBaseModelWithIdNameLabelAndDesc):
  childrenIds: List[str] = []
  memberIds: List[str] = []
  code: Union[AliasCode, None] = None
