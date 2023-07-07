from src.usdm_excel.ncit import NCIt

def test_code(mocker):
    mock_id = mocker.patch("usdm_excel.id_manager.build_id")
    mock_id.side_effect=['Code_1']
    item = NCIt()
    code = item.code(code="CODE", decode="DECODE")
    assert code.id == "Code_1"
    assert code.code == "CODE"
    assert code.codeSystem == "NCI Thesaurus"
    assert code.codeSystemVersion == ""
    assert code.decode == "DECODE"