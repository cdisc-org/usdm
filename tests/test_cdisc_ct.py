from usdm_excel.cdisc_ct_library import CDISCCTLibrary


def test_load(mocker, globals):
    item = CDISCCTLibrary(globals.errors_and_logging)
    assert (item.submission("E-MAIL"))["conceptId"] == "C25170"
    assert (item.preferred_term("E-mail"))["conceptId"] == "C25170"
