from typing import List, Literal
from .alias_code import AliasCode
from .api_base_model import ApiBaseModelWithIdNameAndLabel
from .biomedical_concept_property import BiomedicalConceptProperty
from .comment_annotation import CommentAnnotation


class BiomedicalConcept(ApiBaseModelWithIdNameAndLabel):
    synonyms: List[str] = []
    reference: str
    properties: List[BiomedicalConceptProperty] = []
    code: AliasCode
    notes: List[CommentAnnotation] = []
    instanceType: Literal["BiomedicalConcept"]
