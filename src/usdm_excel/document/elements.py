from usdm_excel.base_sheet import BaseSheet

class Elements():

  def __init__(self, parent: BaseSheet, study):
    super().__init__()
    self.parent = parent
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.methods = [func for func in dir(self.__class__) if callable(getattr(self.__class__, func)) and not func.startswith("_")]

  def valid_method(self, name):
    return name in self.methods

  def study_phase(self):
    phase = self.study_version.phase()
    results = [{'instance': phase, 'klass': 'Code', 'attribute': 'decode'}]
    return self._set_of_references(results)

  def study_short_title(self):
    title = self.study_version.get_title('Brief Study Title')
    results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text'}] if title else []
    return self._set_of_references(results)

  def study_full_title(self):
    title = self.study_version.get_title('Official Study Title')
    results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text'}] if title else []
    return self._set_of_references(results)

  def study_acronym(self):
    title = self.study_version.get_title('Study Acronym')
    results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text'}] if title else []
    return self._set_of_references(results)

  def study_rationale(self):
    results = [{'instance': self.study_version, 'klass': 'StudyVersion', 'attribute': 'rationale'}]
    return self._set_of_references(results)

  def study_version_identifier(self):
    results = [{'instance': self.study_version, 'klass': 'StudyVersion', 'attribute': 'versionIdentifier'}]
    return self._set_of_references(results)

  def study_identifier(self):
    identifier = self.study_version.sponsor_identifier()
    results = [{'instance': identifier, 'klass': 'StudyIdentifier', 'attribute': 'studyIdentifier'}]
    return self._set_of_references(results)

  def study_regulatory_identifiers(self):
    results = []
    identifiers = self.study_version.studyIdentifiers
    for identifier in identifiers:
      if identifier.studyIdentifierScope.organizationType.code == 'C188863' or identifier.studyIdentifierScope.organizationType.code == 'C93453':
        item = {'instance': identifier, 'klass': 'StudyIdentifier', 'attribute': 'studyIdentifier'}
        results.append(item)
    return self._set_of_references(results)

  def study_date(self):
    dates = self.protocol_document_version.dateValues
    for date in dates:
      if date.type.code == 'C99903x1':
        results = [{'instance': date, 'klass': 'GovernanceDate', 'attribute': 'dateValue'}]
        return self._set_of_references(results)
    return []
  
  def approval_date(self):
    dates = self.study_version.dateValues
    for date in dates:
      if date.type.code == 'C132352':
        results = [{'instance': date, 'klass': 'GovernanceDate', 'attribute': 'dateValue'}]
        return self._set_of_references(results)
    return []

  def organization_name_and_address(self):
    identifier = self.study_version.sponsor_identifier()
    results = [
      {'instance': identifier.studyIdentifierScope, 'klass': 'Organization', 'attribute': 'name'},
      {'instance': identifier.studyIdentifierScope.legalAddress, 'klass': 'Address', 'attribute': 'text'},
    ]
    return self._set_of_references(results)

  def organization_address(self):
    identifier = self.study_version.sponsor_identifier()
    results = [
      {'instance': identifier.studyIdentifierScope.legalAddress, 'klass': 'Address', 'attribute': 'text'},
    ]
    return self._set_of_references(results)

  def organization_name(self):
    identifier = self.study_version.sponsor_identifier()
    results = [
      {'instance': identifier.studyIdentifierScope, 'klass': 'Organization', 'attribute': 'name'},
    ]
    return self._set_of_references(results)

  def amendment(self):
    amendments = self.study_version.amendments
    results = [{'instance': amendments[-1], 'klass': 'StudyAmendment', 'attribute': 'number'}]
    return self._set_of_references(results)

  def amendment_scopes(self):
    results = []
    amendment = self.study_version.amendments[-1]
    for item in amendment.enrollments:
      if item.type.code == "C68846":
        results = [{'instance': item.type, 'klass': 'Code', 'attribute': 'decode'}]
        return self._set_of_references(results)
      else:
        entry = {'instance': item.code.standardCode, 'klass': 'Code', 'attribute': 'decode'}
        results.append(entry)
    return self._set_of_references(results)

  def no_value_for_test(self):
    return ""

  # def _sponsor_identifier(self):
  #   identifiers = self.study_version.studyIdentifiers
  #   for identifier in identifiers:
  #     if identifier.studyIdentifierScope.organizationType.code == 'C70793':
  #       return identifier
  #   return None
  
  def _set_of_references(self, items):
    if items:
      return ", ".join([f'<usdm:ref klass="{item["klass"]}" id="{item["instance"].id}" attribute="{item["attribute"]}"/>' for item in items])
    else:
      return ""

  # def _get_title(self, title_type):
  #   for title in self.study_version.titles:
  #     if title.type.decode == title_type:
  #       return title
  #   return None
