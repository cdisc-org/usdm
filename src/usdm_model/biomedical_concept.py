from typing import List
from .alias_code import AliasCode
from .api_base_model import ApiNameModel
from .biomedical_concept_property import BiomedicalConceptProperty

class BiomedicalConcept(ApiNameModel):
  bcSynonyms: List[str] = []
  bcReference: str
  bcProperties: List[BiomedicalConceptProperty] = []
  bcConceptCode: AliasCode
