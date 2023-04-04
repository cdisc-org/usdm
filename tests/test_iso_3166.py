from src.usdm_excel.iso_3166 import ISO3166
from src.usdm_excel.id_manager import id_manager

def test_code():
    id_manager.clear()
    item = ISO3166()
    code = item.code("GB")
    assert code.codeId == "Code_1"
    assert code.code == "GBR"
    assert code.codeSystem == "ISO 3166 1 alpha3"
    assert code.codeSystemVersion == ""
    assert code.decode == "United Kingdom of Great Britain and Northern Ireland"
    code = item.code("GBR")
    assert code.codeId == "Code_2"
    assert code.code == "GBR"
    assert code.codeSystem == "ISO 3166 1 alpha3"
    assert code.codeSystemVersion == ""
    assert code.decode == "United Kingdom of Great Britain and Northern Ireland"
    code = item.code("XXX")
    assert code.codeId == "Code_3"
    assert code.code == "DNK"
    assert code.codeSystem == "ISO 3166 1 alpha3"
    assert code.codeSystemVersion == ""
    assert code.decode == "Denmark"