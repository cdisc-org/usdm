from typing import List, Literal
from .api_base_model import ApiBaseModelWithId
from .code import Code
from .governance_date import GovernanceDate
from .narrative_content import NarrativeContent
from .comment_annotation import CommentAnnotation


class StudyDefinitionDocumentVersion(ApiBaseModelWithId):
    version: str
    status: Code
    dateValues: List[GovernanceDate] = []
    contents: List[NarrativeContent] = []
    notes: List[CommentAnnotation] = []
    instanceType: Literal["StudyDefinitionDocumentVersion"]

    def narrative_content_in_order(self):
        sections = []
        narrative_content = self._first_narrative_content()
        while narrative_content:
            sections.append(narrative_content)
            narrative_content = next(
                (x for x in self.contents if x.id == narrative_content.nextId), None
            )
        return sections

    def _first_narrative_content(self) -> NarrativeContent:
        return next((x for x in self.contents if not x.previousId and x.nextId), None)
