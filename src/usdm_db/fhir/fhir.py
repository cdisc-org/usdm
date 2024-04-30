
from usdm_model.study import Study
from usdm_db.cross_reference import CrossReference
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging
from usdm_db.document.utility import get_soup
from fhir.resources.bundle import Bundle
from fhir.resources.identifier import Identifier
from uuid import uuid4

class FHIR():

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
    # self.chapters = []
    # self.modal_count = 1
    # if self.protocol_document_version.id != self.study.versions[0].documentVersionId:
    #   raise self.LogicError(f"Failed to initialise NarrativeContent for document creation, ids did not match")

  def to_fhir(self, uuid: uuid4):
    try:
      # self.modal_count = 1
      # self.chapters = []
      # root = self.protocol_document_version.contents[0]
      # for id in root.childIds:
      #   content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
      #   if self._is_level_1_doc_section(content.sectionNumber):
      #     self.chapters.append(f'<a href="#section-{content.sectionNumber}"></a>')

      identifier = Identifier(system='urn:ietf:rfc:3986', value=f'urn:uuid:{uuid}')
      bundle = Bundle(id=None, entry=[], type="document", identifier=identifier)
      return bundle.json()
    except Exception as e:
      self._errors_and_logging.exception(f"Exception raised generating FHIR content. See logs for more details", e)
      return None

  # def _content_to_html(self, content, doc, highlight=False):
  #   level = self._get_level(content.sectionNumber)
  #   klass = "page" if level == 1 else ""
  #   heading_id = f"section-{content.sectionNumber}"
  #   if (level == 1 and self._is_first_section(content.sectionNumber)):
  #     with doc.tag('div', klass=klass):
  #       doc.asis(self._table_of_contents())    
  #   with doc.tag('div', klass=klass):
  #     if (self._is_level_1_doc_section(content.sectionNumber)) or (level > 1):
  #       with doc.tag(f'h{level}', id=heading_id):
  #         doc.asis(f"{content.sectionNumber} {content.sectionTitle}")
  #     doc.asis(str(self._translate_references(content.text, highlight)))
  #     for id in content.childIds:
  #       content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
  #       self._content_to_html(content, doc, highlight)

  # def _get_level(self, section_number):
  #   if section_number.lower().startswith("appendix"):
  #     result = 1
  #   else:
  #     text = section_number[:-1] if section_number.endswith('.') else section_number
  #     result = len(text.split('.'))
  #   return result
      
  # def _is_doc_section(self, section_number):
  #   try:
  #     sn = int(section_number)
  #     return True if sn > 0 else False
  #   except:
  #     return True

  # def _is_level_1_doc_section(self, section_number):
  #   level = self._get_level(section_number)
  #   return level == 1 and self._is_doc_section(section_number)
  
  # def _is_first_section(self, section_number):
  #   try:
  #     sn = int(section_number)
  #     return True if sn == 1 else False
  #   except:
  #     return False

  # def _translate_references(self, content_text, highlight=False):
  #   soup = get_soup(content_text, self._errors_and_logging)
  #   for ref in soup(['usdm:ref']):
  #     try:
  #       attributes = ref.attrs
  #       instance = self._cross_ref.get(attributes['klass'], attributes['id'])
  #       value = self._resolve_instance(instance, attributes['attribute'])
  #       translated_text = self._translate_references(value, highlight)
  #       self._replace_and_highlight(soup, ref, translated_text, highlight)
  #     except Exception as e:
  #       self._errors_and_logging.exception(f"Exception raised while attempting to translate reference '{attributes}' while generating the HTML document, see the logs for more info", e)
  #       self._replace_and_highlight(soup, ref, 'Missing content: exception', highlight)
  #   self._errors_and_logging.debug(f"Translate references from {content_text} => {get_soup(str(soup), self._errors_and_logging)}")
  #   return get_soup(str(soup), self._errors_and_logging)

  # def _resolve_instance(self, instance, attribute, highlight=False):
  #   dictionary = self._get_dictionary(instance)
  #   value = str(getattr(instance, attribute))
  #   soup = get_soup(value, self._errors_and_logging)
  #   for ref in soup(['usdm:tag']):
  #     try:
  #       attributes = ref.attrs
  #       if dictionary:
  #         entry = next((item for item in dictionary.parameterMaps if item.tag == attributes['name']), None)
  #         self._replace_and_highlight(soup, ref, get_soup(entry.reference, self._errors_and_logging), highlight)
  #       else:
  #         self._errors_and_logging.error(f"Missing dictionary while attempting to resolve reference '{attributes}' while generating the HTML document")
  #         self._replace_and_highlight(soup, ref, 'Missing content: missing dictionary', highlight)
  #     except Exception as e:
  #       self._errors_and_logging.exception(f"Failed to resolve reference '{attributes} while generating the HTML document", e)
  #       self._replace_and_highlight(soup, ref, 'Missing content: exception', highlight)
  #   return str(soup)

  # def _get_dictionary(self, instance):
  #   try:
  #     return self._cross_ref.get('SyntaxTemplateDictionary', instance.dictionaryId)
  #   except:
  #     return None  

