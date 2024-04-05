from usdm_excel.managers import Managers
from usdm_model.code import Code
from usdm_excel.code_base import CodeBase

class NCIt(CodeBase):

  def __init__(self, managers: Managers):
    super().__init__(managers)

  def code(self, code, decode):
    return Code(id=self._id_manager.build_id(Code), code=code, codeSystem='NCI Thesaurus', codeSystemVersion='24.01e', decode=decode)

