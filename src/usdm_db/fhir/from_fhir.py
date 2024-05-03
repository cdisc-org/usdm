from usdm_model.study_design import StudyDesign
from usdm_model.study import Study
from usdm_model.study_version import StudyVersion
from usdm_model.study_title import StudyTitle
from usdm_model.study_protocol_document import StudyProtocolDocument
from usdm_model.study_protocol_document_version import StudyProtocolDocumentVersion
from usdm_model.code import Code
from usdm_model.study_identifier import StudyIdentifier
from usdm_model.organization import Organization
from usdm_model.address import Address
from usdm_model.narrative_content import NarrativeContent
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging
from usdm_excel.id_manager import IdManager
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.composition import Composition, CompositionSection
from uuid import uuid4

class FromFHIR():

  class LogicError(Exception):
    pass

  def __init__(self, id_manager: IdManager, errors_and_logging: ErrorsAndLogging):
    self._errors_and_logging = ErrorsAndLogging()
    self._id_manager = id_manager

  def from_fhir(self, data: str):
    try:
      bundle = Bundle.parse_raw(data)
      study = self._study(bundle.entry[0].resource.title)
      for item in bundle.entry[0].resource.section:
        self._section(item)
    except Exception as e:
      self._errors_and_logging.exception(f"Exception raised parsing FHIR content. See logs for more details", e)
      return None

  def _section(self, section: CompositionSection):
    print(f"SECTION: {section.title}, {section.code.text}")
    #NarrativeContent(sectionNumber=1, sectionTitle='xxx', text='', childIds=[], previousId=None, nextId=None)
    nc = self._model_instance(NarrativeContent, {'name': f"{section.code.text}", 'sectionNumber': '', 'sectionTitle': section.title, 'text': section.text.div, 'childIds': [], 'previousId': None, 'nextId': None})
    if section.section:
      for item in section.section:
        self._section(item)

  def _study(self, title):
    sponsor_title_code = self._model_instance(Code, {'code': 'C70793', 'decode': '', 'codeSystem': '', 'codeSystemVersion': ''})
    protocl_status_code = self._model_instance(Code, {'code': 'C70793', 'decode': '', 'codeSystem': '', 'codeSystemVersion': ''})
    intervention_model_code = self._model_instance(Code, {'code': 'C70793', 'decode': '', 'codeSystem': '', 'codeSystemVersion': ''})
    study_title = self._model_instance(StudyTitle, {'text': title, 'type': sponsor_title_code})
    protocl_document_version = self._model_instance(StudyProtocolDocumentVersion, {'protocolVersion': '1', 'protocolStatus': protocl_status_code})
    protocl_document = self._model_instance(StudyProtocolDocument, {'name': 'EP1', 'label': 'Epoch A', 'description': '', 'versions': [protocl_document_version]})
    study_design = self._model_instance(StudyDesign, {'name': 'Study Design', 'label': '', 'description': '', 
      'rationale': 'XXX', 'interventionModel': intervention_model_code, 'arms': [], 'studyCells': [], 
      'epochs': [], 'population': None})
    country_code = self._model_instance(Code, {'code': 'C70793', 'decode': '', 'codeSystem': '', 'codeSystemVersion': ''})
    sponsor_code = self._model_instance(Code, {'code': "C70793", 'decode': 'sponsor', 'codeSystem': '', 'codeSystemVersion': ''})
    address = self._model_instance(Address, {'line': 'line 1', 'city': 'City', 'district': 'District', 'state': 'State', 'postalCode': '12345', 'country': country_code})
    organization = self._model_instance(Organization, {'name': 'Sponsor', 'organizationType': sponsor_code, 'identifier': "123456789", 'identifierScheme': "DUNS", 'legalAddress': address}) 
    identifier = self._model_instance(StudyIdentifier, {'studyIdentifier': 'SPONSOR-1234', 'studyIdentifierScope': organization})
    study_version = self._model_instance(StudyVersion, {'versionIdentifier': '1', 'rationale': 'XXX', 'titles': [study_title], 'studyDesigns': [study_design], 
                                                     'documentVersionId': protocl_document_version.id, 'studyIdentifiers': [identifier]}) 
    study = self._model_instance(Study, {'id': uuid4(), 'name': 'Study', 'label': '', 'description': '', 'versions': [study_version], 'documentedBy': protocl_document}) 
    return study

  def _model_instance(self, cls, params):
    params['id'] = params['id'] if 'id' in params else self._id_manager.build_id(cls)
    params['instanceType'] = cls.__name__
    return cls(**params)