from typing import List, Union
from .api_base_model import ApiBaseModel
from .alias_code import AliasCode

class BiomedicalConceptCategory(ApiBaseModel):
  biomedicalConceptCategoryId: str
  bcCategoryChildIds: List[str] = []
  bcCategoryName: str
  bcCategoryDescription: Union[str, None] = None
  bcCategoryMemberIds: List[str] = []
  bcCategoryCode: Union[AliasCode, None] = None
