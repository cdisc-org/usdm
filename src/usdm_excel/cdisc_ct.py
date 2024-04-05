from usdm_excel.managers import Managers
from usdm_excel.cdisc_ct_library import CDISCCTLibrary
from usdm_excel.code_base import CodeBase

class CDISCCT(CodeBase):

  def __init__(self, managers: Managers):
    super().__init__(managers)
    self._library = self._managers.cdisc_ct_library
    
  def code(self, code, decode):
    return self._build(code=code, system=self._library.system, version=self._library.version, decode=decode)
 
  def code_for_attribute(self, klass, attribute, value):
    item = self._library.klass_and_attribute(klass, attribute, value)
    if item:
      return self._build(code=item['conceptId'], system=self._library.system, version=self._library.version, decode=item['preferredTerm'])
    else:
      return None

  def code_for_unit(self, value):
    item = self._library.unit(value)
    if item == None:
      return None
    return self._build(code=item['conceptId'], system=self._library.system, version=self._library.version, decode=item['preferredTerm'])
