from typing import Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc

class BiomedicalConceptSurrogate(ApiBaseModelWithIdNameLabelAndDesc):
  reference: Union[str, None] = None
  instanceType: Literal['BiomedicalConceptSurrogate'] = 'BiomedicalConceptSurrogate'
