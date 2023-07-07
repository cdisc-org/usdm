from typing import Union
from uuid import UUID
from .api_base_model import ApiIdModel
from .organisation import Organisation

class StudyIdentifier(ApiIdModel):
  studyIdentifier: str
  studyIdentifierScope: Organisation
