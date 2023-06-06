from typing import Union
from uuid import UUID
from .api_base_model import ApiBaseModel
from .organisation import Organisation

class StudyIdentifier(ApiBaseModel):
  studyIdentifierId: str
  studyIdentifier: str
  studyIdentifierScope: Organisation
