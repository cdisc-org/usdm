from .elements import Elements
from .utility import usdm_reference
from usdm_model.study import Study
from usdm_db.errors.errors import Errors

class TemplateBase():

  def __init__(self, study: Study, errors: Errors):
    self._errors = errors
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.elements = Elements(study, errors)
    self.methods = [func for func in dir(self.__class__) if callable(getattr(self.__class__, func)) and not func.startswith("_")]

  def valid_method(self, name):
    result = name in self.methods
    if not result:
      self._errors.add(f"Could not resolve method name, {name} not in {self.methods}", Errors.WARNING)
    return result
  
  def _reference(self, item, attribute):
    return usdm_reference(item, attribute)

  def _add_checking_for_tag(self, doc, tag, text):
    doc.asis(text)