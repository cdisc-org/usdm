from usdm_excel.id_manager import IdManager
from usdm_excel.cross_ref import CrossRef
from usdm_model.code import Code

class CodeBase():

  def __init__(self, id_manager: IdManager, cross_references: CrossRef):
    self._id_manager = id_manager
    self._cross_references = cross_references

  def _build(self, code, system, version, decode):
    id = self._id_manager.build_id(Code)
    instance = Code(id=id, code=code, codeSystem=system, codeSystemVersion=version, decode=decode)
    self._cross_references.add(instance.id, instance)
    return instance
 