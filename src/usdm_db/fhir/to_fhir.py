from usdm_model.study import Study
from usdm_model.narrative_content import NarrativeContent
from usdm_db.cross_reference import CrossReference
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging
from usdm_db.document.utility import get_soup
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.identifier import Identifier
from fhir.resources.composition import Composition, CompositionSection
from fhir.resources.narrative import Narrative
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.reference import Reference
from uuid import uuid4
import datetime

class ToFHIR():

  class LogicError(Exception):
    pass

  def __init__(self, doc_title: str, study: Study, errors_and_logging: ErrorsAndLogging):
    self.study = study
    self._errors_and_logging = ErrorsAndLogging()
    self._cross_ref = CrossReference(study, self._errors_and_logging)
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.doc_title = doc_title

  def to_fhir(self, uuid: uuid4):
    try:
      sections = []
      root = self.protocol_document_version.contents[0]
      for id in root.childIds:
        content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
        sections.append(self._content_to_section(content))
      type_code = CodeableConcept(text=f"EvidenceReport")
      #date = datetime.datetime.now().isoformat()
      date = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
      author = Reference(display="USDM")
      composition = Composition(title=self.doc_title, type=type_code, section=sections, date=date, status="preliminary", author=[author])
      identifier = Identifier(system='urn:ietf:rfc:3986', value=f'urn:uuid:{uuid}')
      bundle_entry = BundleEntry(resource=composition, fullUrl="https://www.example.com/Composition/1234")
      bundle = Bundle(id=None, entry=[bundle_entry], type="document", identifier=identifier, timestamp=date)
      return bundle.json()
    except Exception as e:
      self._errors_and_logging.exception(f"Exception raised generating FHIR content. See logs for more details", e)
      return None

  def _content_to_section(self, content: NarrativeContent) -> CompositionSection:
    div = self._translate_references(content.text)
    narrative = Narrative(status='generated', div=self._add_section_heading(content, div))
    title = self._format_section_title(content.sectionTitle)
    code = CodeableConcept(text=f"section{content.sectionNumber}-{title}")
    #print(f"COMPOSITION: {code.text}, {title}, {narrative}, {div}")
    section = CompositionSection(title=content.sectionTitle, code=code, text=narrative, section=[])
    for id in content.childIds:
      content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
      child = self._content_to_section(content)
      section.section.append(child)
    return section

  def _format_section_title(self, title: str) -> str:
    return title.lower().strip().replace(' ', '-')
  
  def _clean_section_number(self, section_number: str) -> str:
    return section_number[:-1] if section_number.endswith('.') else section_number
  
  def _translate_references(self, content_text: str):
    soup = get_soup(content_text, self._errors_and_logging)
    for ref in soup(['usdm:ref']):
      try:
        attributes = ref.attrs
        instance = self._cross_ref.get(attributes['klass'], attributes['id'])
        value = self._resolve_instance(instance, attributes['attribute'])
        translated_text = self._translate_references(value)
        self._replace_and_highlight(ref, translated_text)
      except Exception as e:
        self._errors_and_logging.exception(f"Exception raised while attempting to translate reference '{attributes}' while generating the FHIR message, see the logs for more info", e)
        self._replace_and_highlight(ref, 'Missing content: exception')
    self._errors_and_logging.debug(f"Translate references from {content_text} => {get_soup(str(soup), self._errors_and_logging)}")
    return get_soup(str(soup), self._errors_and_logging)

  def _resolve_instance(self, instance, attribute):
    dictionary = self._get_dictionary(instance)
    value = str(getattr(instance, attribute))
    soup = get_soup(value, self._errors_and_logging)
    for ref in soup(['usdm:tag']):
      try:
        attributes = ref.attrs
        if dictionary:
          entry = next((item for item in dictionary.parameterMaps if item.tag == attributes['name']), None)
          if entry:
            self._replace_and_highlight(ref, get_soup(entry.reference, self._errors_and_logging))
          else:
            self._errors_and_logging.error(f"Missing dictionary entry while attempting to resolve reference '{attributes}' while generating the FHIR message")
            self._replace_and_highlight(ref, 'Missing content: missing dictionary entry')
        else:
          self._errors_and_logging.error(f"Missing dictionary while attempting to resolve reference '{attributes}' while generating the FHIR message")
          self._replace_and_highlight(ref, 'Missing content: missing dictionary')
      except Exception as e:
        self._errors_and_logging.exception(f"Failed to resolve reference '{attributes} while generating the FHIR message", e)
        self._replace_and_highlight(ref, 'Missing content: exception')
    return str(soup)

  def _replace_and_highlight(self, ref, text):
    ref.replace_with(text)

  def _get_dictionary(self, instance):
    try:
      return self._cross_ref.get('SyntaxTemplateDictionary', instance.dictionaryId)
    except:
      return None  

  def _add_section_heading(self, content, div):
    DIV_OPEN_NS = '<div xmlns="http://www.w3.org/1999/xhtml">'
    text = str(div)
    text = text.replace(DIV_OPEN_NS, f"{DIV_OPEN_NS}<p>{content.sectionNumber} {content.sectionTitle}</p>")
    return text
