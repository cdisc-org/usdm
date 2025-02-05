from typing import List, Literal, Union
from pydantic import Field
from .api_base_model import ApiBaseModel
from .study_definition_document import StudyDefinitionDocument
from .study_version import StudyVersion
from uuid import UUID


class Study(ApiBaseModel):
    id: Union[UUID, None] = None
    name: str = Field(min_length=1)
    description: Union[str, None] = None
    label: Union[str, None] = None
    versions: List[StudyVersion] = []
    documentedBy: List[StudyDefinitionDocument] = []
    instanceType: Literal["Study"]

    def document_by_template_name(self, name: str) -> StudyDefinitionDocument:
        # for x in self.documentedBy:
        #   print(f"DOC: {x.templateName}, {name}")
        return next(
            (x for x in self.documentedBy if x.templateName.upper() == name.upper()),
            None,
        )
