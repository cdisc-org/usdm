import pytest
from src.usdm_excel.cdisc_biomedical_concept import CDISCBiomedicalConcepts

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

def test__bc_as_usdm(mocker):
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['C1', 'BC_1', 'A1', 'C2', 'BC_2', 'A2']
  item = CDISCBiomedicalConcepts()
  data = {
    'conceptId': 'X1',
    'shortName': 'Name',
    'synonym': ['shortie'],
    '_links': { 'self': { 'href': 'link' } }
  }
  bc = item._bc_as_usdm(data)
  assert(bc.id) == 'BC_1'
  assert(bc.bcName) == 'Name'
  assert(bc.bcSynonyms) == ['shortie']
  assert(bc.bcReference) == 'link'
  assert(bc.bcConceptCode.id) == 'A1'
  assert(bc.bcConceptCode.standardCode.id) == 'C1'
  assert(bc.bcConceptCode.standardCode.code) == 'X1'
  assert(bc.bcConceptCode.standardCode.decode) == 'Name'
  assert(bc.bcConceptCode.standardCode.codeSystem) == "NCI Thesaurus"
  assert(bc.bcConceptCode.standardCode.codeSystemVersion) == "" 
  assert(bc.bcConceptCode.standardCodeAliases) == []
  data = {
    'conceptId': 'X2',
    'shortName': 'Name1',
    '_links': { 'self': { 'href': 'link' } }
  }
  bc = item._bc_as_usdm(data)
  assert(bc.id) == 'BC_2'
  assert(bc.bcName) == 'Name1'
  assert(bc.bcSynonyms) == []

@xfail
def test__bc_property_as_usdm(self, property, codes):
  assert 0
