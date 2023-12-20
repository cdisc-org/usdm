from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .study_protocol_document_version import StudyProtocolDocumentVersion

class StudyProtocolDocument(ApiBaseModelWithIdNameLabelAndDesc):
  versions: List[StudyProtocolDocumentVersion] = []
  instanceType: Literal['StudyProtocolDocument'] = 'StudyProtocolDocument'
