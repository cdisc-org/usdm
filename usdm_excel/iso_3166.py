from usdm_excel.id_manager import IdManager
from usdm.code import Code
import json

class ISO3166():

  def __init__(self, id_manager: IdManager):
    self.id_manager = id_manager
    f = open('data/iso_3166.json', 'r')
    self.db = json.load(f)

  def code(self, code):
    decode = self._get_decode(code)
    if decode == None:
      code = 'DNK'
      decode = 'Denmark'
    return Code(codeId=self.id_manager.build_id(Code), code=code, codeSystem='ISO 3166 1 alpha3', codeSystemVersion="", decode=decode)

  def _get_decode(self, code):
    entry = next((item for item in self.db if item['alpha-3'] == code), None)
    if entry == None:
      return None
    else:
      return entry['name']