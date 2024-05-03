# from usdm_model.study import Study
# from usdm_model.narrative_content import NarrativeContent
# from usdm_db.cross_reference import CrossReference
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging
# from usdm_db.document.utility import get_soup
from fhir.resources.bundle import Bundle, BundleEntry
# from fhir.resources.identifier import Identifier
# from fhir.resources.composition import Composition, CompositionSection
# from fhir.resources.narrative import Narrative
# from fhir.resources.codeableconcept import CodeableConcept
# from fhir.resources.reference import Reference
# from uuid import uuid4
# import datetime

class FromFHIR():

  class LogicError(Exception):
    pass

  def __init__(self, errors_and_logging: ErrorsAndLogging):
    self._errors_and_logging = ErrorsAndLogging()

  def from_fhir(self, data: str):
    try:
      bundle = Bundle.model_validate(data)
    except Exception as e:
      self._errors_and_logging.exception(f"Exception raised parsing FHIR content. See logs for more details", e)
      return None

