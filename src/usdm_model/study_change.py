from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .document_content_reference import DocumentContentReference


class StudyChange(ApiBaseModelWithIdNameLabelAndDesc):
    summary: str
    rationale: str
    changedSections: List[DocumentContentReference]
    instanceType: Literal["StudyChange"]
