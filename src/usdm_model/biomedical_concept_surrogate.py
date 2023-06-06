from typing import List, Union
from .api_base_model import ApiBaseModel

class BiomedicalConceptSurrogate(ApiBaseModel):
  bcSurrogateId: str
  bcSurrogateName: str
  bcSurrogateDescription: Union[str, None] = None
  bcSurrogateReference: str
