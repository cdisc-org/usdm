from typing import List
from .alias_code import AliasCode
from .api_base_model import ApiBaseModelWithIdAndName
from .biomedical_concept_property import BiomedicalConceptProperty

class BiomedicalConcept(ApiBaseModelWithIdAndName):
  bcSynonyms: List[str] = []
  bcReference: str
  bcProperties: List[BiomedicalConceptProperty] = []
  bcConceptCode: AliasCode
