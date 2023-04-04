import pytest

from src.usdm_excel.ncit import NCIt
from src.usdm_excel.id_manager import id_manager

def test_code():
    id_manager.clear()
    item = NCIt()
    code = item.code(code="CODE", decode="DECODE")
    assert code.codeId == "Code_1"
    assert code.code == "CODE"
    assert code.codeSystem == "NCI Thesaurus"
    assert code.codeSystemVersion == ""
    assert code.decode == "DECODE"