from typing import List, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .study_protocol_document_version import StudyProtocolDocumentVersion

class StudyProtocolDocument(ApiBaseModelWithIdNameLabelAndDesc):
  versions: List[StudyProtocolDocumentVersion] = []
