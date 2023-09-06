from typing import List
from .alias_code import AliasCode
from .api_base_model import ApiBaseModelWithIdNameAndLabel
from .biomedical_concept_property import BiomedicalConceptProperty

class BiomedicalConcept(ApiBaseModelWithIdNameAndLabel):
  bcSynonyms: List[str] = []
  bcReference: str
  bcProperties: List[BiomedicalConceptProperty] = []
  code: AliasCode
