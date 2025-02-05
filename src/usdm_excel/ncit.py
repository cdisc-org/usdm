from usdm_excel.globals import Globals
from usdm_model.code import Code
from usdm_excel.code_base import CodeBase


class NCIt(CodeBase):
    def __init__(self, globals: Globals):
        super().__init__(globals)

    def code(self, code, decode):
        return Code(
            id=self._id_manager.build_id(Code),
            code=code,
            codeSystem="NCI Thesaurus",
            codeSystemVersion="24.01e",
            decode=decode,
        )
