import pytest
import pandas as pd

from usdm_excel.study_design_sites_sheet.study_design_sites_sheet import StudyDesignSitesSheet
from usdm_excel.cross_ref import cross_references
from usdm_model.code import Code

def test_create(mocker):
  cross_references.clear()
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['Code_1', 'Org_1', 'Addr_1', 'Id_1', 'Code_2', 'Org_2', 'Addr_2', 'Id_2', 'Code_3', 'Org_3', 'Addr_3', 'Id_3']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    [ 'CRO1', 'CRO One',   'Study Registry', 'DUNS', '111111111', 'line|district|city|state|postal_code|GBR',      'Site1', 'Site One', 'Big Site' ],
    [ 'CRO2', 'CRO Two',   'Study Registry', 'DUNS', '222222222', 'line2,district2,city2,state2,postal_code2,FRA', 'Site2', 'Site Two', 'Little Site'],
    [ 'CRO3', 'CRO Three', 'Study Registry', 'DUNS', '333333333', 'line3,district3,city3,state3,postal_code3,FR',  'Site3', 'Site Three', 'Middle Site']
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['name', 'label', 'type', 'identifierScheme', 'identifier', 'address', 'siteName', 'siteLabel', 'siteDescription'])
  mock_json = mocker.patch("json.load")
  mock_json.return_value = {}
  expected_1 = Code(id='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="GBR")
  expected_2 = Code(id='Code2', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
  expected_3 = Code(id='Code3', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
  mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
  mock_code.side_effect=[expected_1, expected_2, expected_3]
  sites = StudyDesignSitesSheet("")
  assert len(sites.items) == 3
  assert sites.items[0].id == 'Id_1'
  assert sites.items[0].studyIdentifier == 'NCT12345678'
  assert sites.items[0].studyIdentifierScope.name == 'ClinicalTrials.gov'
  assert sites.items[0].studyIdentifierScope.legalAddress.city == 'city'
  assert sites.items[1].id == 'Id_2'
  assert sites.items[1].studyIdentifier == 'NCT12345679'
  assert sites.items[1].studyIdentifierScope.name == 'ClinicalTrials2.gov'
  assert sites.items[1].studyIdentifierScope.legalAddress.city == 'city2'
  assert sites.items[2].id == 'Id_3'
  assert sites.items[2].studyIdentifier == 'NCT123456710'
  
def test_create_new_columns(mocker):
  cross_references.clear()
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['Code_1', 'Org_1', 'Addr_1', 'Id_1', 'Code_2', 'Org_2', 'Addr_2', 'Id_2', 'Code_3', 'Org_3', 'Addr_3', 'Id_3']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    [ 'USGOV', 'CT-GOV', 'ClinicalTrials.gov', 'CT.gov [1]', 'Study Registry', 'NCT12345678', 'line|district|city|state|postal_code|GBR' ],
    [ 'USGOV2', 'CT-GOV2', 'ClinicalTrials2.gov', '', 'Study Registry', 'NCT12345679', 'line2,district2,city2,state2,postal_code2,FRA' ],
    [ 'USGOV3', 'CT-GOV3', 'ClinicalTrials3.gov', 'CT.gov [3]', 'Study Registry', 'NCT123456710', 'line3,district3,city3,state3,postal_code3,FR' ]
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['organisationIdentifierScheme', 'organisationIdentifier', 'name', 'label', 'type', 'studyIdentifier', 'organisationAddress'])
  mock_json = mocker.patch("json.load")
  mock_json.return_value = {}
  expected_1 = Code(id='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="GBR")
  expected_2 = Code(id='Code2', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
  expected_3 = Code(id='Code3', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
  mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
  mock_code.side_effect=[expected_1, expected_2, expected_3]
  sites = StudyIdentifiersSheet("")
  assert len(sites.items) == 3
  assert sites.items[0].id == 'Id_1'
  assert sites.items[0].studyIdentifier == 'NCT12345678'
  assert sites.items[0].studyIdentifierScope.name == 'ClinicalTrials.gov'
  assert sites.items[0].studyIdentifierScope.label == 'CT.gov [1]'
  assert sites.items[0].studyIdentifierScope.legalAddress.city == 'city'
  assert sites.items[1].id == 'Id_2'
  assert sites.items[1].studyIdentifier == 'NCT12345679'
  assert sites.items[1].studyIdentifierScope.name == 'ClinicalTrials2.gov'
  assert sites.items[1].studyIdentifierScope.legalAddress.city == 'city2'
  assert sites.items[1].studyIdentifierScope.label == ''
  assert sites.items[2].id == 'Id_3'
  assert sites.items[2].studyIdentifier == 'NCT123456710'
  
def test_create_empty(mocker):
  cross_references.clear()
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyIdentifierName', 'studyIdentifierDescription', 'studyIdentifierType'])
  sites = StudyIdentifiersSheet("")
  assert len(sites.items) == 0

def test_read_cell_by_name_error(mocker):
  cross_references.clear()
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['Id 1', 'Id One']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyIdentifierName', 'studyIdentifierDescription'])
  sites = StudyIdentifiersSheet("")
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyIdentifiers"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "Exception 'Failed to detect column(s) 'organisationType, type' in sheet' raised reading sheet."
  
def test_address_error(mocker):
  cross_references.clear()
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
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
  sites = StudyIdentifiersSheet("")
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyIdentifiers"
  assert mock_error.call_args[0][1] == 1
  assert mock_error.call_args[0][2] == 6
  assert mock_error.call_args[0][3] == "Address does not contain the required fields (line, district, city, state, postal code and country code) using '|' separator characters, only 5 found"
