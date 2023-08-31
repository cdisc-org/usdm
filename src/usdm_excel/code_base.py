from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_model.code import Code

class CodeBase():

  def _build(self, code, system, version, decode):
    instance = Code(id=id_manager.build_id(Code), code=code, codeSystem=system, codeSystemVersion=version, decode=decode)
    cross_references.add(instance.id, instance)
    return instance
 