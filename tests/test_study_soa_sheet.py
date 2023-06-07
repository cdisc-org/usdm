import pytest
import pandas as pd

from src.usdm_excel.study_soa_sheet.study_soa_sheet import StudySoASheet
from usdm_excel.study_soa_sheet.timepoint_type import TimepointType
from usdm_excel.iso_8601_duration import ISO8601Duration
from src.usdm_excel.base_sheet import BaseSheet

def test_timepoint_type(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  mock_read = mocker.patch("pandas.read_excel")
  data = { 'col_1': [ 'A:', 'P: 2D ', 'P2:2D', 'C:', 'N3: 3 weeks', 'N: +2 days', 'P: -3 hrs' ] }
  mock_read.return_value = pd.DataFrame.from_dict(data)
  parent = BaseSheet("", "")
  test_data = [
    (0,0,'anchor', 0, "", ISO8601Duration.ZERO_DURATION),
    (1,0,'previous', -1, "2D", "P2D"),
    (2,0,'previous', -2, "2D", "P2D"),
    (3,0,'cycle start', 1, "", ISO8601Duration.ZERO_DURATION),
    (4,0,'next', 3, "3 weeks", "P3W"),
    (5,0,'next', 1, "+2 days", "P2D"),
    (6,0,'previous', -1, "-3 hrs", "PT3H"),
  ]
  for index, test in enumerate(test_data):
    print(f"IDX {index}")
    item = TimepointType(parent, test[0], test[1])
    assert(item.timing_type) == test[2]
    assert(item.relative_ref) == test[3]
    assert(item.description) == test[4]
    assert(item.value) == test[5]

def test_timepoint_type_error(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  mock_read = mocker.patch("pandas.read_excel")
  data = { 'col_1': [ 'A', 'P: 2 ', '', 'P2: 2 decades' ] }
  mock_read.return_value = pd.DataFrame.from_dict(data)
  parent = BaseSheet("", "Sheet X")
  test_data = [
    (0,0,"Could not decode the timing value, no ':' detected in 'A'"),
    (1,0,"Could not decode the duration value, no value and units found in '2'"),
    (2,0,"Could not decode the timing value, cell was empty"),
    (3,0,"Could not decode the duration value '2 decades'"),
  ]
  for index, test in enumerate(test_data):
    mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
    item = TimepointType(parent, test[0], test[1])
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "Sheet X"
    assert mock_error.call_args[0][1] == test[0] + 1
    assert mock_error.call_args[0][2] == test[1] + 1
    assert mock_error.call_args[0][3] == test[2]

# def test_create(mocker):
#   mock_id = mocker.patch("usdm_excel.id_manager.build_id")
#   mock_id.side_effect=['Code_1', 'Org_1', 'Addr_1', 'Id_1', 'Code_2', 'Org_2', 'Addr_2', 'Id_2', 'Code_3', 'Org_3', 'Addr_3', 'Id_3']
#   mocked_open = mocker.mock_open(read_data="File")
#   mocker.patch("builtins.open", mocked_open)
#   data = [
#     [ 'USGOV', 'CT-GOV', 'ClinicalTrials.gov', 'Study Registry', 'NCT12345678', 'line|city|district|state|postal_code|GBR' ],
#     [ 'USGOV2', 'CT-GOV2', 'ClinicalTrials2.gov', 'Study Registry', 'NCT12345679', 'line2,city2,district2,state2,postal_code2,FRA' ],
#     [ 'USGOV3', 'CT-GOV3', 'ClinicalTrials3.gov', 'Study Registry', 'NCT123456710', 'line3,city3,district3,state3,postal_code3,FR' ]
#   ]
#   mock_read = mocker.patch("pandas.read_excel")
#   mock_read.return_value = pd.DataFrame(data, columns=['organisationIdentifierScheme', 'organisationIdentifier', 'organisationName', 'organisationType', 'studyIdentifier', 'organisationAddress'])
#   mock_json = mocker.patch("json.load")
#   mock_json.return_value = {}
#   expected_1 = Code(codeId='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="GBR")
#   expected_2 = Code(codeId='Code2', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
#   expected_3 = Code(codeId='Code3', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
#   mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
#   mock_code.side_effect=[expected_1, expected_2, expected_3]
#   ids = StudyIdentifiersSheet("")
#   assert len(ids.identifiers) == 3
#   assert ids.identifiers[0].studyIdentifierId == 'Id_1'
#   assert ids.identifiers[0].studyIdentifier == 'NCT12345678'
#   assert ids.identifiers[0].studyIdentifierScope.organisationName == 'ClinicalTrials.gov'
#   assert ids.identifiers[0].studyIdentifierScope.organizationLegalAddress.city == 'city'
#   assert ids.identifiers[1].studyIdentifierId == 'Id_2'
#   assert ids.identifiers[1].studyIdentifier == 'NCT12345679'
#   assert ids.identifiers[1].studyIdentifierScope.organisationName == 'ClinicalTrials2.gov'
#   assert ids.identifiers[1].studyIdentifierScope.organizationLegalAddress.city == 'city2'
#   assert ids.identifiers[2].studyIdentifierId == 'Id_3'
#   assert ids.identifiers[2].studyIdentifier == 'NCT123456710'
  
# def test_create_empty(mocker):
#   mocked_open = mocker.mock_open(read_data="File")
#   mocker.patch("builtins.open", mocked_open)
#   data = []
#   mock_read = mocker.patch("pandas.read_excel")
#   mock_read.return_value = pd.DataFrame(data, columns=['studyIdentifierName', 'studyIdentifierDescription', 'studyIdentifierType'])
#   ids = StudyIdentifiersSheet("")
#   assert len(ids.identifiers) == 0

# def test_read_cell_by_name_error(mocker):
#   mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
#   mocked_open = mocker.mock_open(read_data="File")
#   mocker.patch("builtins.open", mocked_open)
#   data = [['Id 1', 'Id One']]
#   mock_read = mocker.patch("pandas.read_excel")
#   mock_read.return_value = pd.DataFrame(data, columns=['studyIdentifierName', 'studyIdentifierDescription'])
#   ids = StudyIdentifiersSheet("")
#   mock_error.assert_called()
#   assert mock_error.call_args[0][0] == "studyIdentifiers"
#   assert mock_error.call_args[0][1] == None
#   assert mock_error.call_args[0][2] == None
#   assert mock_error.call_args[0][3] == "Exception ['organisationType'] raised reading sheet."
  
# def test_address_error(mocker):
#   mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
#   mock_id = mocker.patch("usdm_excel.id_manager.build_id")
#   mock_id.side_effect=['Code_1', 'Org_1', 'Addr_1', 'Id_1']
#   mocked_open = mocker.mock_open(read_data="File")
#   mocker.patch("builtins.open", mocked_open)
#   data = [
#     [ 'USGOV', 'CT-GOV', 'ClinicalTrials.gov', 'Study Registry', 'NCT12345678', 'line|city|district|state|GBR' ],
#   ]
#   mock_read = mocker.patch("pandas.read_excel")
#   mock_read.return_value = pd.DataFrame(data, columns=['organisationIdentifierScheme', 'organisationIdentifier', 'organisationName', 'organisationType', 'studyIdentifier', 'organisationAddress'])
#   mock_json = mocker.patch("json.load")
#   mock_json.return_value = {}
#   expected_1 = Code(codeId='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="GBR")
#   mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
#   mock_code.side_effect=[expected_1]
#   ids = StudyIdentifiersSheet("")
#   mock_error.assert_called()
#   assert mock_error.call_args[0][0] == "studyIdentifiers"
#   assert mock_error.call_args[0][1] == 1
#   assert mock_error.call_args[0][2] == 6
#   assert mock_error.call_args[0][3] == "Address does not contain the required fields (line, city, district, state, postal code and country code) using '|' separator characters, only 5 found"
