from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .alias_code import AliasCode

class BiomedicalConceptCategory(ApiBaseModelWithIdNameLabelAndDesc):
  childIds: List[str] = []
  memberIds: List[str] = []
  code: Union[AliasCode, None] = None
  instanceType: Literal['BiomedicalConceptCategory']
