from src.usdm_excel.iso_3166 import ISO3166

def test_code(mocker):
    mock_id = mocker.patch("usdm_excel.id_manager.build_id")
    mock_id.side_effect=['Code_1', 'Code_2', 'Code_3']
    item = ISO3166()
    code = item.code("GB")
    assert code.id == "Code_1"
    assert code.code == "GBR"
    assert code.codeSystem == "ISO 3166 1 alpha3"
    assert code.codeSystemVersion == "2020-08"
    assert code.decode == "United Kingdom of Great Britain and Northern Ireland"
    code = item.code("GBR")
    assert code.id == "Code_2"
    assert code.code == "GBR"
    assert code.codeSystem == "ISO 3166 1 alpha3"
    assert code.codeSystemVersion == "2020-08"
    assert code.decode == "United Kingdom of Great Britain and Northern Ireland"
    code = item.code("XXX")
    assert code.id == "Code_3"
    assert code.code == "DNK"
    assert code.codeSystem == "ISO 3166 1 alpha3"
    assert code.codeSystemVersion == "2020-08"
    assert code.decode == "Denmark"