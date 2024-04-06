from usdm_excel.cdisc_ct_library import CDISCCTLibrary
from tests.test_factory import Factory

factory = Factory()
globals = factory.globals

def test_load(mocker):
    item = CDISCCTLibrary(globals.errors, globals.logger)
    assert(item.submission('E-MAIL'))['conceptId'] == 'C25170' 
    assert(item.preferred_term('E-mail'))['conceptId'] == 'C25170' 