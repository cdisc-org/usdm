from usdm_excel.id_manager import id_manager
from usdm.code import Code
import json
import os

class ISO3166():

  def __init__(self):
    #f = open('data/iso_3166.json', 'r')
    f = open(os.path.join(os.path.dirname(__file__), 'data', 'iso_3166.json'))
    self.db = json.load(f)

  def code(self, code):
    code, decode = self._get_decode(code)
    if code == None:
      code = 'DNK'
      decode = 'Denmark'
    return Code(codeId=id_manager.build_id(Code), code=code, codeSystem='ISO 3166 1 alpha3', codeSystemVersion='', decode=decode)

  def _get_decode(self, code):
    if len(code) == 2:
      field = 'alpha-2'
    else:
      field = 'alpha-3'
    entry = next((item for item in self.db if item[field] == code), None)
    if entry == None:
      return None, None
    else:
      return entry['alpha-3'], entry['name']