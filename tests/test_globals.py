from usdm_excel.globals import Globals


def test_create():
    globals = Globals()
    globals.create()
    assert globals.errors_and_logging is not None
    assert globals.id_manager is not None
    assert globals.ct_version_manager is not None
    assert globals.option_manager is not None
    assert globals.cross_references is not None
    assert globals.cdisc_ct_library is not None
    assert globals.template_manager is not None
