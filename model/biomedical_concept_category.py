from typing import List
from .api_base_model import ApiBaseModel

class BiomedicalConceptCategory(ApiBaseModel):
  biomedicalConceptCategoryId: str
  bcCategoryParentIds: List[str] = []
  bcCategoryChildrenIds: List[str] = []
  bcCategoryName: str
  bcCategoryDescription: str
  bcCategoryMemberIds: List[str] = []
