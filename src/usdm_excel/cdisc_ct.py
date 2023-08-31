from usdm_excel.cdisc_ct_library import cdisc_ct_library
from usdm_excel.code_base import CodeBase

class CDISCCT(CodeBase):

  API_ROOT = 'https://api.library.cdisc.org/api'  

  def code(self, code, decode):
    return self._build(code=code, system=cdisc_ct_library.system, version=cdisc_ct_library.version, decode=decode)
 
  def code_for_attribute(self, klass, attribute, value):
    item = cdisc_ct_library.klass_and_attribute(klass, attribute, value)
    if item == None:
      return None
    return self._build(code=item['conceptId'], system=cdisc_ct_library.system, version=cdisc_ct_library.version, decode=item['preferredTerm'])
