from usdm_excel.id_manager import IdManager
from usdm_excel.cross_ref import CrossRef
from usdm_excel.cdisc_ct_library import CDISCCTLibrary
from usdm_excel.code_base import CodeBase

class CDISCCT(CodeBase):

  def __init__(self, id_manager: IdManager, cross_references: CrossRef, ct_library: CDISCCTLibrary):
    super().__init__(id_manager, cross_references)
    self._library = ct_library
    
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
