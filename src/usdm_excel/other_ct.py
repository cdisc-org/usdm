from usdm_excel.cdisc_ct_library import cdisc_ct_library
from usdm_excel.code_base import CodeBase

class OtherCT(CodeBase):

  def code(self, code, system, version, decode):
    return self._build(code=code, system=system, version=version, decode=decode)
 