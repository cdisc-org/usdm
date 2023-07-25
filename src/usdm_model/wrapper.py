from .api_base_model import ApiBaseModel
from .study import Study

class Wrapper(ApiBaseModel):
  study: Study
