from src.usdm_excel.cdisc_ct_library import CDISCCTLibrary

def test_load(mocker):
    item = CDISCCTLibrary()
    assert(item.submission('E-MAIL'))['conceptId'] == 'C25170' 
    assert(item.preferred_term('E-mail'))['conceptId'] == 'C25170' 