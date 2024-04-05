from usdm_excel.ncit import NCIt

def test_code(mocker):
    mock_id = mocker.patch("usdm_excel.self.managers.id_manager.build_id")
    mock_id.side_effect=['Code_1']
    item = NCIt()
    code = item.code(code="CODE", decode="DECODE")
    assert code.id == "Code_1"
    assert code.code == "CODE"
    assert code.codeSystem == "NCI Thesaurus"
    assert code.codeSystemVersion == "24.01e"
    assert code.decode == "DECODE"