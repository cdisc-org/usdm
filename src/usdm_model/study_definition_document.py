from typing import List, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .study_definition_document_version import StudyDefinitionDocumentVersion
from .code import Code
from .comment_annotation import CommentAnnotation


class StudyDefinitionDocument(ApiBaseModelWithIdNameLabelAndDesc):
    language: Code
    type: Code
    templateName: str
    versions: List[StudyDefinitionDocumentVersion] = []
    childIds: List[str] = []
    notes: List[CommentAnnotation] = []
    instanceType: Literal["StudyDefinitionDocument"]
