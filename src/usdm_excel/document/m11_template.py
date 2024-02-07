import re
# import os
# import base64
# import traceback
# import docraptor
# import warnings
from yattag import Doc
from .elements import Elements
from usdm_excel.cross_ref import cross_references
# from usdm_excel.logger import 
# from usdm_excel.errors.errors import error_manager

class M11Template():

  def __init__(self, study):
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.elements = Elements(study)
    #warnings.filterwarnings("error")
    # self.filepath = filepath
    # self.study = study
    # self.study_version = study.versions[0]
    # self.study_design = self.study_version.studyDesigns[0]
    # self.protocol_document_version = self.study.documentedBy.versions[0]
    # self.doc_title = doc_title
    # if self.protocol_document_version.id != self.study.versions[0].documentVersionId:
    #   logging.error(f"Failed to initialise NarrativeContent for document creation, ids did not match")
    #   raise self.LogicError(f"Failed to initialise NarrativeContent for document creation, ids did not match")


  def title_page(self):
    #print(f"M11 TP:")
    doc = Doc()
    with doc.tag('table'):
      self._title_page_entry(doc, 'Sponsor Confidentiality Statement:', '')
      self._title_page_entry(doc, 'Full Title:', f'{self.elements.study_full_title()}')
      self._title_page_entry(doc, 'Trial Acronym:', f'{self.elements.study_acronym()}')
      self._title_page_entry(doc, 'Protocol Identifier:', f'{self.elements.study_identifier()}')
      self._title_page_entry(doc, 'Original Protocol:', '')
      self._title_page_entry(doc, 'Version Number:', f'{self.elements.study_version_identifier()}')
      self._title_page_entry(doc, 'Version Date:', f'{self.elements.study_date()}')
      self._title_page_entry(doc, 'Amendment Identifier:', f'{self.elements.amendment()}')
      self._title_page_entry(doc, 'Amendment Scope:', f'{self.elements.amendment_scopes()}')
      self._title_page_entry(doc, 'Compound Codes(s):', '')
      self._title_page_entry(doc, 'Compound Name(s):', '')
      self._title_page_entry(doc, 'Trial Phase:', f'{self.elements.study_phase()}')
      self._title_page_entry(doc, 'Short Title:', f'{self.elements.study_short_title()}')
      self._title_page_entry(doc, 'Sponsor Name and Address:', f'{self.elements.organization_name_and_address()}')
      self._title_page_entry(doc, 'Regulatory Agency Identifier Number(s):', f'{self.elements.study_regulatory_identifiers()}')
      self._title_page_entry(doc, 'Spondor Approval Date:', f'{self.elements.approval_date()}')

      # Enter Nonproprietary Name(s)
      # Enter Proprietary Name(s)
      # Globally/Locally/Cohort
      # Primary Reason for Amendment
      # Region Identifier
      # Secondary Reason for Amendment

    result = doc.getvalue()
    #print(f"DOC: {result}")
    return result
  
  def criteria(self, type):
    #print(f"M11 TP:")
    heading = { 
      'C25532': "Patients may be included in the study only if they meet <strong>all</strong> the following criteria:",
      'C25370': "Patients may be excluded in the study for <strong>any</strong> of the following reasons:",
    }
    doc = Doc()
    with doc.tag('p'):
      doc.asis(heading[type])  
    with doc.tag('table'):
      for criterion in self._criteria_list(type):
        self._critieria_entry(doc, criterion['identifier'], criterion['text'])
    return doc.getvalue()

  def objective_endpoints(self):
    #print(f"M11 TP:")
    doc = Doc()
    with doc.tag('table'):
      for item in self._objective_endpoints_list():
        self._objective_endpoints_entry(doc, item['objective'], item['endpoints'])
    return doc.getvalue()

  def _critieria_entry(self, doc, number, entry):
    with doc.tag('tr'):
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(number)  
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(entry)

  def _objective_endpoints_entry(self, doc, objective, endpoints):
    with doc.tag('tr'):
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(objective)  
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        for endpoint in endpoints:
          with doc.tag('p'):
            doc.asis(endpoint)

  def _title_page_entry(self, doc, title, entry):
    with doc.tag('tr'):
      with doc.tag('th', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(title)  
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(entry)

  # def _sponsor_identifier(self):
  #   identifiers = self.study_version.studyIdentifiers
  #   for identifier in identifiers:
  #     if identifier.studyIdentifierScope.organizationType.code == 'C70793':
  #       return identifier
  #   return None
  
  # def _study_phase(self):
  #   phase = self.study_version.studyPhase.standardCode
  #   results = [{'instance': phase, 'klass': 'Code', 'attribute': 'decode', 'path': 'StudyVersion/@studyPhase/@standardCode/@decode'}]
  #   return self._set_of_references(results)

  # def _study_short_title(self):
  #   title = self._get_title('Brief Study Title')
  #   results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text', 'path': 'StudyVersion/@titles/StudyTitle/@text'}]
  #   return self._set_of_references(results)

  # def _study_full_title(self):
  #   title = self._get_title('Official Study Title')
  #   results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text', 'path': 'StudyVersion/@titles/StudyTitle/@text'}]
  #   return self._set_of_references(results)

  # def _study_acronym(self):
  #   title = self._get_title('Study Acronym')
  #   results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text', 'path': 'StudyVersion/@titles/StudyTitle/@text'}]
  #   return self._set_of_references(results)

  # def _study_rationale(self):
  #   results = [{'instance': self.study_version, 'klass': 'StudyVersion', 'attribute': 'rationale', 'path': 'StudyVersion/@rationale'}]
  #   return self._set_of_references(results)

  # def _study_version(self):
  #   results = [{'instance': self.study_version, 'klass': 'StudyVersion', 'attribute': 'versionIdentifier', 'path': 'StudyVersion/@versionIdentifier'}]
  #   return self._set_of_references(results)

  # def _study_identifier(self):
  #   identifier = self._sponsor_identifier()
  #   results = [{'instance': identifier, 'klass': 'StudyIdentifier', 'attribute': 'studyIdentifier', 'path': 'StudyIdentifier[Organization/@type/@code=C70793]/@studyIdentifier'}]
  #   return self._set_of_references(results)

  # def _study_regulatory_identifiers(self):
  #   results = []
  #   identifiers = self.study_version.studyIdentifiers
  #   for identifier in identifiers:
  #     if identifier.studyIdentifierScope.organizationType.code == 'C188863' or identifier.studyIdentifierScope.organizationType.code == 'C93453':
  #       item = {'instance': identifier, 'klass': 'StudyIdentifier', 'attribute': 'studyIdentifier', 'path': 'StudyIdentifier[Organization/@type/@code=C188863|C93453]/@studyIdentifier'}
  #       results.append(item)
  #   return self._set_of_references(results)

  # def _study_date(self):
  #   dates = self.protocol_document_version.dateValues
  #   for date in dates:
  #     if date.type.code == 'C99903x1':
  #       results = [{'instance': date, 'klass': 'GovernanceDate', 'attribute': 'dateValue', 'path': 'StudyProtocolDocumentVersion/GovernanceDate[@type/@code=C99903x1]/@dateValue'}]
  #       return self._set_of_references(results)
  #   return []
  
  # def _approval_date(self):
  #   dates = self.study_version.dateValues
  #   for date in dates:
  #     if date.type.code == 'C132352':
  #       results = [{'instance': date, 'klass': 'GovernanceDate', 'attribute': 'dateValue', 'path': 'StudyVersion/GovernanceDate[@type/@code=C132352]/@dateValue'}]
  #       return self._set_of_references(results)
  #   return []

  # def _organization_name_and_address(self):
  #   identifier = self._sponsor_identifier()
  #   results = [
  #     {'instance': identifier.studyIdentifierScope, 'klass': 'Organization', 'attribute': 'name', 'path': 'StudyIdentifier[Organization/@type/@code=C70793]/Organization/@name'},
  #     {'instance': identifier.studyIdentifierScope.legalAddress, 'klass': 'Address', 'attribute': 'text', 'path': 'StudyIdentifier[Organization/@type/@code=C70793]/Organization/Address/@text'},
  #   ]
  #   return self._set_of_references(results)

  # def _amendment(self):
  #   amendments = self.study_version.amendments
  #   results = [{'instance': amendments[-1], 'klass': 'StudyAmendment', 'attribute': 'number', 'path': 'StudyVersion/StudyAmendment/@number'}]
  #   return self._set_of_references(results)

  # def _amendment_scopes(self):
  #   results = []
  #   amendment = self.study_version.amendments[-1]
  #   for item in amendment.enrollments:
  #     if item.type.code == "C68846":
  #       results = [{'instance': item.type, 'klass': 'Code', 'attribute': 'decode', 'path': 'StudyVersion/StudyAmendment/SubjectEnrollment[@type/@code=C68846]/Code/@decode'}]
  #       return self._set_of_references(results)
  #     else:
  #       entry = {'instance': item.code.standardCode, 'klass': 'Code', 'attribute': 'decode', 'path': 'StudyVersion/StudyAmendment/SubjectEnrollment/@code/@standardCode/@decode'}
  #       results.append(entry)
  #   return self._set_of_references(results)

  # def _no_value_for_test(self):
  #   return []

  def _criteria_list(self, type):
    results = []
    items = [c for c in self.study_design.population.criteria if c.category.code == type ]
    items.sort(key=lambda d: d.identifier)
    for item in items:
      result = {'identifier': item.identifier, 'text': item.text}
      dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', item.dictionaryId)
      if dictionary:
        result['text'] = self._substitute_tags(result['text'], dictionary)
      results.append(result)
    return results

  def _objective_endpoints_list(self):
    results = []
    for item in self.study_design.objectives:
      result = {'objective': item.text, 'endpoints': []}
      dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', item.dictionaryId)
      if dictionary:
        result['objective'] = self._substitute_tags(result['objective'], dictionary)
      for endpoint in item.endpoints:
        dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', endpoint.dictionaryId)
        ep_text = endpoint.text
        if dictionary:
          ep_text = self._substitute_tags(ep_text, dictionary)
        result['endpoints'].append(ep_text)
      results.append(result)
    return results

  def _substitute_tags(self, text, dictionary):
      tags = re.findall(r'\[([^]]*)\]', text)
      for tag in tags:
        if tag in dictionary.parameterMap:
          map = dictionary.parameterMap[tag]
          text = text.replace(f"[{tag}]", f'<usdm:ref klass="{map["klass"]}" id="{map["id"]}" attribute="{map["attribute"]}"/>')
      return text

  # def _list_references(self, content_text):
  #   references = []
  #   soup = BeautifulSoup(content_text, 'html.parser')
  #   for ref in soup(['usdm:ref']):
  #     attributes = ref.attrs
  #     if 'path' in attributes:
  #       path = f"{attributes['path']}"
  #     else:
  #       path = f"{attributes['klass']}/@{attributes['attribute']}"
  #     if path not in references:
  #       references.append(path)
  #   return references if references else ['No mapping path']
  
  # def _set_of_references(self, items):
  #   if items:
  #     return ", ".join([f'<usdm:ref klass="{item["klass"]}" id="{item["instance"].id}" attribute="{item["attribute"]}" path="{item["path"]}"/>' for item in items])
  #   else:
  #     return ""

  # def _get_title(self, title_type):
  #   for title in self.study_version.titles:
  #     if title.type.decode == title_type:
  #       return title
  #   return None
