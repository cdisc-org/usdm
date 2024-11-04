from typing import Literal
from .api_base_model import ApiBaseModelWithId

class DocumentContentReference(ApiBaseModelWithId):
  sectionNumber: str
  sectionTitle: str
  instanceType: Literal['DocumentContentReference']
