from usdm_excel.managers import Managers
from usdm_model.code import Code

class CodeBase():

  def __init__(self, managers: Managers):
    self._managers = managers
    self._id_manager = managers.id_manager
    self._cross_references = managers.cross_references

  def _build(self, code, system, version, decode):
    id = self._id_manager.build_id(Code)
    instance = Code(id=id, code=code, codeSystem=system, codeSystemVersion=version, decode=decode)
    self._cross_references.add(instance.id, instance)
    return instance
 