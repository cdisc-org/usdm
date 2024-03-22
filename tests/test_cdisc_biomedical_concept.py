import pytest
from usdm_excel.cdisc_biomedical_concept import CDISCBiomedicalConcepts

xfail = pytest.mark.xfail

# def test_code(mocker):
#     mock_id = mocker.patch("usdm_excel.id_manager.build_id")
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
  
def test__url():
  item = CDISCBiomedicalConcepts()
  assert (item._url('something')) == f"{CDISCBiomedicalConcepts.API_ROOT}something"

@xfail
def test__bc_as_usdm(mocker):
  assert 0

@xfail
def test__bc_property_as_usdm(self, property, codes):
  assert 0
