import pandas as pd
from usdm_excel.study_identifier_and_organization_sheets.study_identifiers_sheet import StudyIdentifiersSheet
from usdm_model.code import Code
from usdm_model.organization import Organization
from usdm_model.address import Address
from tests.test_factory import Factory

def test_create(mocker, globals):
  globals.cross_references.clear()
  organizations(globals)
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Id_1', 'Id_2', 'Id_3']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    [ 'NCT12345678', 'Sponsor1' ],
    [ 'NCT12345679', 'Sponsor2' ],
    [ 'NCT123456710', 'Sponsor3' ]
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['identifier', 'organization'])
  item = StudyIdentifiersSheet("", globals)
  assert len(item.items) == 3
  assert item.items[0].model_dump() == {
    'id': 'Id_1',
    'instanceType': 'StudyIdentifier',
    'scopeId': 'Organization_1',
    'text': 'NCT12345678',
  }
  assert item.items[1].model_dump() == {
    'id': 'Id_2',
    'instanceType': 'StudyIdentifier',
    'scopeId': 'Organization_2',
    'text': 'NCT12345679',
  }
  assert item.items[2].model_dump() == {
    'id': 'Id_3',
    'instanceType': 'StudyIdentifier',
    'scopeId': 'Organization_3',
    'text': 'NCT123456710',
  }

def test_create_with_z(mocker, globals):
  globals.cross_references.clear()
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Code_1', 'Org_1', 'Addr_1', 'Id_1', 'Code_2', 'Org_2', 'Addr_2', 'Id_2', 'Code_3', 'Org_3', 'Addr_3', 'Id_3']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    [ 'NCT12345678', 'line|district|city|state|postal_code|GBR' ],
    [ 'NCT12345679', 'line2,district2,city2,state2,postal_code2,FRA' ],
    [ 'NCT123456710', 'line3,district3,city3,state3,postal_code3,FR' ]
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['organizationIdentifierScheme', 'organizationIdentifier', 'organizationName', 'organizationType', 'studyIdentifier', 'organizationAddress'])
  mock_json = mocker.patch("json.load")
  mock_json.return_value = {}
  expected_1 = Code(id='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="GBR")
  expected_2 = Code(id='Code2', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
  expected_3 = Code(id='Code3', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
  mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
  mock_code.side_effect=[expected_1, expected_2, expected_3]
  ids = StudyIdentifiersSheet("", globals)
  assert len(ids.identifiers) == 3
  assert len(ids.organizations) == 3
  assert ids.identifiers[0].id == 'Id_1'
  assert ids.identifiers[0].text == 'NCT12345678'
  assert ids.organizations[0].name == 'ClinicalTrials.gov'
  assert ids.organizations[0].legalAddress.city == 'city'
  assert ids.identifiers[1].id == 'Id_2'
  assert ids.identifiers[1].text == 'NCT12345679'
  assert ids.organizations[1].name == 'ClinicalTrials2.gov'
  assert ids.organizations[1].legalAddress.city == 'city2'
  assert ids.identifiers[2].id == 'Id_3'
  assert ids.identifiers[2].text == 'NCT123456710'
  
def test_create_new_columns(mocker, globals):
  globals.cross_references.clear()
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Code_1', 'Org_1', 'Addr_1', 'Id_1', 'Code_2', 'Org_2', 'Addr_2', 'Id_2', 'Code_3', 'Org_3', 'Addr_3', 'Id_3']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    [ 'USGOV', 'CT-GOV', 'ClinicalTrials.gov', 'CT.gov [1]', 'Study Registry', 'NCT12345678', 'line|district|city|state|postal_code|GBR' ],
    [ 'USGOV2', 'CT-GOV2', 'ClinicalTrials2.gov', '', 'Study Registry', 'NCT12345679', 'line2,district2,city2,state2,postal_code2,FRA' ],
    [ 'USGOV3', 'CT-GOV3', 'ClinicalTrials3.gov', 'CT.gov [3]', 'Study Registry', 'NCT123456710', 'line3,district3,city3,state3,postal_code3,FR' ]
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['IdentifierScheme', 'organisationIdentifier', 'name', 'label', 'type', 'studyIdentifier', 'address'])
  mock_json = mocker.patch("json.load")
  mock_json.return_value = {}
  expected_1 = Code(id='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="GBR")
  expected_2 = Code(id='Code2', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
  expected_3 = Code(id='Code3', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
  mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
  mock_code.side_effect=[expected_1, expected_2, expected_3]
  ids = StudyIdentifiersSheet("", globals)
  assert len(ids.identifiers) == 3
  assert ids.identifiers[0].id == 'Id_1'
  assert ids.identifiers[0].text == 'NCT12345678'
  assert ids.organizations[0].name == 'ClinicalTrials.gov'
  assert ids.organizations[0].label == 'CT.gov [1]'
  assert ids.organizations[0].legalAddress.city == 'city'
  assert ids.identifiers[1].id == 'Id_2'
  assert ids.identifiers[1].text == 'NCT12345679'
  assert ids.organizations[1].name == 'ClinicalTrials2.gov'
  assert ids.organizations[1].legalAddress.city == 'city2'
  assert ids.organizations[1].label == ''
  assert ids.identifiers[2].id == 'Id_3'
  assert ids.identifiers[2].text == 'NCT123456710'
  
def test_create_empty(mocker, globals):
  globals.cross_references.clear()
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyIdentifierName', 'studyIdentifierDescription', 'studyIdentifierType'])
  ids = StudyIdentifiersSheet("", globals)
  assert len(ids.identifiers) == 0

def test_read_cell_by_name_error(mocker, globals):
  globals.cross_references.clear()
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['Id 1', 'Id One']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyIdentifierName', 'studyIdentifierDescription'])
  ids = StudyIdentifiersSheet("", globals)
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyIdentifiers"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "Exception. Error [Failed to detect column(s) 'organisationType, organizationType, type' in sheet] while reading sheet 'studyIdentifiers'. See log for additional details."
  
def test_address_error(mocker, globals):
  globals.cross_references.clear()
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Code_1', 'Org_1', 'Addr_1', 'Id_1']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    [ 'USGOV', 'CT-GOV', 'ClinicalTrials.gov', 'Study Registry', 'NCT12345678', 'line|city|district|state|GBR' ],
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['organisationIdentifierScheme', 'organisationIdentifier', 'organisationName', 'organisationType', 'studyIdentifier', 'organisationAddress'])
  mock_json = mocker.patch("json.load")
  mock_json.return_value = {}
  expected_1 = Code(id='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="GBR")
  mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
  mock_code.side_effect=[expected_1]
  ids = StudyIdentifiersSheet("", globals)
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyIdentifiers"
  assert mock_error.call_args[0][1] == 1
  assert mock_error.call_args[0][2] == 6
  assert mock_error.call_args[0][3] == "Address 'line|city|district|state|GBR' does not contain the required fields (lines, district, city, state, postal code and country code) using '|' separator characters, only 5 found"

def organizations(globals):
  factory = Factory(globals)
  org1 = factory.item(Organization, {'name': 'Sponsor1', 'type': factory.cdisc_code("C70793", "sponsor"), 'identifier': "123456781", 'identifierScheme': "DUNS", 'legalAddress': None}) 
  org2 = factory.item(Organization, {'name': 'Sponsor2', 'type': factory.cdisc_code("C70793", "sponsor"), 'identifier': "123456782", 'identifierScheme': "DUNS", 'legalAddress': None}) 
  org3 = factory.item(Organization, {'name': 'Sponsor3', 'type': factory.cdisc_code("C70793", "sponsor"), 'identifier': "123456783", 'identifierScheme': "DUNS", 'legalAddress': None}) 
  globals.cross_references.add(org1.name, org1)
  globals.cross_references.add(org2.name, org2)
  globals.cross_references.add(org3.name, org3)
  