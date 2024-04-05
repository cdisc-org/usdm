from usdm_excel.managers import Managers
from usdm_model.code import Code

class CodeBase():

  def __init__(self, managers: Managers):
    self._managers = managers

  def _build(self, code, system, version, decode):
    id = self._managers.id_manager.build_id(Code)
    instance = Code(id=id, code=code, codeSystem=system, codeSystemVersion=version, decode=decode)
    self._managers.cross_references.add(instance.id, instance)
    return instance
 