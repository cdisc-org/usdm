# import re
# import os
# import base64
# import traceback
# import docraptor
# import warnings
# from yattag import Doc
# from bs4 import BeautifulSoup   
# from usdm_excel.cross_ref import cross_references
# from usdm_excel.logger import logging
# from usdm_excel.errors.errors import error_manager

class Elements():

  def __init__(self, study):
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]

  def study_phase(self):
    phase = self.study_version.studyPhase.standardCode
    results = [{'instance': phase, 'klass': 'Code', 'attribute': 'decode', 'path': 'StudyVersion/@studyPhase/@standardCode/@decode'}]
    return self._set_of_references(results)

  def study_short_title(self):
    title = self._get_title('Brief Study Title')
    results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text', 'path': 'StudyVersion/@titles/StudyTitle/@text'}]
    return self._set_of_references(results)

  def study_full_title(self):
    title = self._get_title('Official Study Title')
    results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text', 'path': 'StudyVersion/@titles/StudyTitle/@text'}]
    return self._set_of_references(results)

  def study_acronym(self):
    title = self._get_title('Study Acronym')
    results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text', 'path': 'StudyVersion/@titles/StudyTitle/@text'}]
    return self._set_of_references(results)

  def study_rationale(self):
    results = [{'instance': self.study_version, 'klass': 'StudyVersion', 'attribute': 'rationale', 'path': 'StudyVersion/@rationale'}]
    return self._set_of_references(results)

  def study_version_identifier(self):
    results = [{'instance': self.study_version, 'klass': 'StudyVersion', 'attribute': 'versionIdentifier', 'path': 'StudyVersion/@versionIdentifier'}]
    return self._set_of_references(results)

  def study_identifier(self):
    identifier = self._sponsor_identifier()
    results = [{'instance': identifier, 'klass': 'StudyIdentifier', 'attribute': 'studyIdentifier', 'path': 'StudyIdentifier[Organization/@type/@code=C70793]/@studyIdentifier'}]
    return self._set_of_references(results)

  def study_regulatory_identifiers(self):
    results = []
    identifiers = self.study_version.studyIdentifiers
    for identifier in identifiers:
      if identifier.studyIdentifierScope.organizationType.code == 'C188863' or identifier.studyIdentifierScope.organizationType.code == 'C93453':
        item = {'instance': identifier, 'klass': 'StudyIdentifier', 'attribute': 'studyIdentifier', 'path': 'StudyIdentifier[Organization/@type/@code=C188863|C93453]/@studyIdentifier'}
        results.append(item)
    return self._set_of_references(results)

  def study_date(self):
    dates = self.protocol_document_version.dateValues
    for date in dates:
      if date.type.code == 'C99903x1':
        results = [{'instance': date, 'klass': 'GovernanceDate', 'attribute': 'dateValue', 'path': 'StudyProtocolDocumentVersion/GovernanceDate[@type/@code=C99903x1]/@dateValue'}]
        return self._set_of_references(results)
    return []
  
  def approval_date(self):
    dates = self.study_version.dateValues
    for date in dates:
      if date.type.code == 'C132352':
        results = [{'instance': date, 'klass': 'GovernanceDate', 'attribute': 'dateValue', 'path': 'StudyVersion/GovernanceDate[@type/@code=C132352]/@dateValue'}]
        return self._set_of_references(results)
    return []

  def organization_name_and_address(self):
    identifier = self._sponsor_identifier()
    results = [
      {'instance': identifier.studyIdentifierScope, 'klass': 'Organization', 'attribute': 'name', 'path': 'StudyIdentifier[Organization/@type/@code=C70793]/Organization/@name'},
      {'instance': identifier.studyIdentifierScope.legalAddress, 'klass': 'Address', 'attribute': 'text', 'path': 'StudyIdentifier[Organization/@type/@code=C70793]/Organization/Address/@text'},
    ]
    return self._set_of_references(results)

  def amendment(self):
    amendments = self.study_version.amendments
    results = [{'instance': amendments[-1], 'klass': 'StudyAmendment', 'attribute': 'number', 'path': 'StudyVersion/StudyAmendment/@number'}]
    return self._set_of_references(results)

  def amendment_scopes(self):
    results = []
    amendment = self.study_version.amendments[-1]
    for item in amendment.enrollments:
      if item.type.code == "C68846":
        results = [{'instance': item.type, 'klass': 'Code', 'attribute': 'decode', 'path': 'StudyVersion/StudyAmendment/SubjectEnrollment[@type/@code=C68846]/Code/@decode'}]
        return self._set_of_references(results)
      else:
        entry = {'instance': item.code.standardCode, 'klass': 'Code', 'attribute': 'decode', 'path': 'StudyVersion/StudyAmendment/SubjectEnrollment/@code/@standardCode/@decode'}
        results.append(entry)
    return self._set_of_references(results)

  def no_value_for_test(self):
    return []

  def _sponsor_identifier(self):
    identifiers = self.study_version.studyIdentifiers
    for identifier in identifiers:
      if identifier.studyIdentifierScope.organizationType.code == 'C70793':
        return identifier
    return None

  # def _criteria(self, type):
  #   results = []
  #   items = [c for c in self.study_design.population.criteria if c.category.code == type ]
  #   items.sort(key=lambda d: d.identifier)
  #   for item in items:
  #     result = {'identifier': item.identifier, 'text': item.text}
  #     dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', item.dictionaryId)
  #     if dictionary:
  #       result['text'] = self._substitute_tags(result['text'], dictionary)
  #     results.append(result)
  #   return results

  # def _objective_endpoints(self):
  #   results = []
  #   for item in self.study_design.objectives:
  #     result = {'objective': item.text, 'endpoints': []}
  #     dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', item.dictionaryId)
  #     if dictionary:
  #       result['objective'] = self._substitute_tags(result['objective'], dictionary)
  #     for endpoint in item.endpoints:
  #       dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', endpoint.dictionaryId)
  #       ep_text = endpoint.text
  #       if dictionary:
  #         ep_text = self._substitute_tags(ep_text, dictionary)
  #       result['endpoints'].append(ep_text)
  #     results.append(result)
  #   return results

  # def _substitute_tags(self, text, dictionary):
  #     tags = re.findall(r'\[([^]]*)\]', text)
  #     for tag in tags:
  #       if tag in dictionary.parameterMap:
  #         map = dictionary.parameterMap[tag]
  #         text = text.replace(f"[{tag}]", f'<usdm:ref klass="{map["klass"]}" id="{map["id"]}" attribute="{map["attribute"]}"/>')
  #     return text

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
  
  def _set_of_references(self, items):
    if items:
      return ", ".join([f'<usdm:ref klass="{item["klass"]}" id="{item["instance"].id}" attribute="{item["attribute"]}" path="{item["path"]}"/>' for item in items])
    else:
      return ""

  def _get_title(self, title_type):
    for title in self.study_version.titles:
      if title.type.decode == title_type:
        return title
    return None
