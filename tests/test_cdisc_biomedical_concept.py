import pytest
from usdm_excel.cdisc_bc_library import CDISCBCLibrary

xfail = pytest.mark.xfail

# def test_code(mocker, globals):
#     mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
#     mock_id.side_effect=['Code_1']
#     item = NCIt()
#     code = item.code(code="CODE", decode="DECODE")
#     assert code.codeId == "Code_1"
#     assert code.code == "CODE"
#     assert code.codeSystem == "NCI Thesaurus"
#     assert code.codeSystemVersion == ""
#     assert code.decode == "DECODE"


@xfail
def test_create():
    assert 0


@xfail
def test_exists():
    assert 0


@xfail
def test_catalogue():
    assert 0


@xfail
def test_usdm():
    assert 0


@xfail
def test__get_package_metadata():
    assert 0


@xfail
def test__get_package_items(self):
    assert 0


def test__url(globals):
    item = CDISCBCLibrary(
        globals.errors_and_logging, globals.cdisc_ct_library, globals.id_manager
    )
    assert (item._url("something")) == f"{CDISCBCLibrary.API_ROOT}something"


@xfail
def test__bc_as_usdm(mocker, globals):
    assert 0


@xfail
def test__bc_property_as_usdm(self, property, codes):
    assert 0
