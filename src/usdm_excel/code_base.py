from usdm_excel.globals import Globals
from usdm_model.code import Code


class CodeBase:
    def __init__(self, globals: Globals):
        self._globals = globals
        self._id_manager = globals.id_manager
        self._cross_references = globals.cross_references

    def _build(self, code, system, version, decode):
        id = self._id_manager.build_id(Code)
        instance = Code(
            id=id,
            code=code,
            codeSystem=system,
            codeSystemVersion=version,
            decode=decode,
        )
        self._cross_references.add(instance.id, instance)
        return instance
