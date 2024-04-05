#from usdm_excel.id_manager import id_manager
from usdm_model.code import Code

class NCIt():

  def __init__(self):
    self.id_manager = id_manager

  def code(self, code, decode):
    return Code(id=self.managers.id_manager.build_id(Code), code=code, codeSystem='NCI Thesaurus', codeSystemVersion='24.01e', decode=decode)

