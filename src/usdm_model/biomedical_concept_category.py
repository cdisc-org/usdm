from typing import List, Union
from .api_base_model import ApiNameDescriptionModel
from .alias_code import AliasCode

class BiomedicalConceptCategory(ApiNameDescriptionModel):
  bcCategoryChildIds: List[str] = []
  bcCategoryMemberIds: List[str] = []
  bcCategoryCode: Union[AliasCode, None] = None
