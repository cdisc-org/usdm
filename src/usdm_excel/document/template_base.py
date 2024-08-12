from .utility import usdm_reference
from usdm_model.study import Study
from usdm_excel.base_sheet import BaseSheet

class TemplateBase():

  def __init__(self, parent: BaseSheet, study: Study, template_name: str):
    self.parent = parent
    self._study = study
    self._study_version = self._study.versions[0]
    self._study_design = self._study_version.studyDesigns[0]
    self._document = self._study.document_by_template_name(template_name)
    self._document_version = self._document.versions[0]
    # self.study = study
    # self.study_version = study.versions[0]
    # self.study_design = self.study_version.studyDesigns[0]
    # self.protocol_document_version = self.study.documentedBy.versions[0]
    #self._elements = Elements(parent, study)
    self._methods = [func for func in dir(self.__class__) if callable(getattr(self.__class__, func)) and not func.startswith("_")]

  def valid_method(self, name):
    result = name in self._methods
    if not result:
      self.parent._general_warning(f"Could not resolve method name, {name} not in {self.methods}")
    return result
  
  def _reference(self, item, attribute):
    return usdm_reference(item, attribute)

  def _add_checking_for_tag(self, doc, tag, text):
    doc.asis(text)