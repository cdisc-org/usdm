from typing import Union
from .api_base_model import ApiBaseModel
from .study import Study


class Wrapper(ApiBaseModel):
    study: Study
    usdmVersion: str
    systemName: Union[str, None] = None
    systemVersion: Union[str, None] = None
