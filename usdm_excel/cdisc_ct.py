from usdm_excel.id_manager import IdManager
from usdm.code import Code
import requests
import os
import yaml

class CDISCCT():

  API_ROOT = 'https://api.library.cdisc.org/api'  

  def __init__(self, id_manager: IdManager):
    self.id_manager = id_manager

  def code(self, code, decode):
    return Code(codeId=self.id_manager.build_id(Code), code=code, codeSystem="http://www.cdisc.org", codeSystemVersion="2022-12-16", decode=decode)
 