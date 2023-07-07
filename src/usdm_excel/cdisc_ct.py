from usdm_excel.id_manager import id_manager
from usdm_model.code import Code
import requests
import os
import yaml
from usdm_excel.cdisc_ct_library import cdisc_ct_library

class CDISCCT():

  API_ROOT = 'https://api.library.cdisc.org/api'  

  def code(self, code, decode):
    return Code(id=id_manager.build_id(Code), code=code, codeSystem=cdisc_ct_library.system, codeSystemVersion=cdisc_ct_library.version, decode=decode)
 
  def code_for_attribute(self, klass, attribute, value):
    item = cdisc_ct_library.klass_and_attribute(klass, attribute, value)
    if item == None:
      return None
    return Code(id=id_manager.build_id(Code), code=item['conceptId'], codeSystem=cdisc_ct_library.system, codeSystemVersion=cdisc_ct_library.version, decode=item['preferredTerm'])
