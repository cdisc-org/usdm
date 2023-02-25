from typing import List
from .api_base_model import ApiBaseModel

class BiomedicalConceptSurrogate(ApiBaseModel):
  bcSurrogateId: str
  bcSurrogateName: str
  bcSurrogateDescription: str
  bcSurrogateReference: str
