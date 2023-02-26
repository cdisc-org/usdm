from usdm_excel.id_manager import IdManager
from usdm.code import Code

class ISO3166():

  def __init__(self, id_manager: IdManager):
    self.id_manager = id_manager

  def code(self, code, decode):
    return Code(codeId=self.id_manager.build_id(Code), code=code, codeSystem="ISO 3166 1 alpha3", codeSystemVersion="", decode=decode)
