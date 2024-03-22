from typing import Union
from .api_base_model import ApiBaseModel
from .study import Study

class Wrapper(ApiBaseModel):
  study: Study
  usdm_version: str
  system_name: Union[str, None] = None
  system_version: Union[str, None] = None