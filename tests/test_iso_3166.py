from usdm_excel.iso_3166 import ISO3166


def test_code(mocker, globals):
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Code_1", "Code_2", "Code_3"]
    item = ISO3166(globals)
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


def test_region_code(mocker, globals):
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Code_1", "Code_2", "Code_3", "Code_4"]
    item = ISO3166(globals)
    code = item.region_code("Americas")
    assert code.id == "Code_1"
    assert code.code == "019"
    assert code.codeSystem == "ISO 3166 1 alpha3"
    assert code.codeSystemVersion == "2020-08"
    assert code.decode == "Americas"
    code = item.region_code("South America")
    assert code.id == "Code_2"
    assert code.code == "005"
    assert code.codeSystem == "ISO 3166 1 alpha3"
    assert code.codeSystemVersion == "2020-08"
    assert code.decode == "South America"
    code = item.region_code("Western Africa")
    assert code.id == "Code_3"
    assert code.code == "011"
    assert code.codeSystem == "ISO 3166 1 alpha3"
    assert code.codeSystemVersion == "2020-08"
    assert code.decode == "Western Africa"
    code = item.region_code("XXX")
    assert code.id == "Code_4"
    assert code.code == "150"
    assert code.codeSystem == "ISO 3166 1 alpha3"
    assert code.codeSystemVersion == "2020-08"
    assert code.decode == "Europe"
