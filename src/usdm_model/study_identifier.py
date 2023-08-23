from .api_base_model import ApiIdModel
from .organization import Organization

class StudyIdentifier(ApiIdModel):
  studyIdentifier: str
  studyIdentifierScope: Organization
