import pandas as pd
from usdm_excel.study_identifiers_sheet.study_references_sheet import StudyReferencesSheet
from usdm_model.code import Code

DEFAULT_COLUMNS = ['identifierScheme', 'organisationIdentifier', 'name', 'label', 'type', 'studyIdentifier', 'address', 'referenceType']
MISSING_COLUMN =  ['identifierScheme', 'organisationIdentifier', 'name', 'label', 'type', 'studyIdentifier', 'address']

def test_create(mocker, globals):
  expected_1 = ('{"id": "RI_1", "text": "NCT12345678", "scope": '
                  '{"id": "Org_1", "name": "ClinicalTrials.gov", "label": "CT.gov Study Registry", '
                   '"organizationType": {"id": "Code_1", "code": "C93453", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Study Registry", "instanceType": "Code"}, '
                   '"identifierScheme": "USGOV", "identifier": "CT-GOV", '
                   '"legalAddress": {"id": "Addr_1", "text": "line, city, district, state, postal_code, Denmark", "line": "line", "city": "city", "district": "district", "state": "state", "postalCode": "postal_code", '
                     '"country": {"id": "Code_2", "code": "DNK", "codeSystem": "ISO 3166 1 alpha3", "codeSystemVersion": "2020-08", "decode": "Denmark", "instanceType": "Code"}, '
                     '"instanceType": "Address"}, '
                   '"instanceType": "Organization"}, '
                '"instanceType": "ReferenceIdentifier", '
                '"type": {"id": "Code_3", "code": "C99910x1", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Pediatric Investigation Plan", "instanceType": "Code"}}'
  )
  expected_2 = ('{"id": "RI_2", "text": "NCT12345679", "scope": '
                  '{"id": "Org_2", "name": "ClinicalTrials2.gov", "label": "CT.gov Registry", '
                   '"organizationType": {"id": "Code_4", "code": "C93453", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Study Registry", "instanceType": "Code"}, '
                   '"identifierScheme": "USGOV2", "identifier": "CT-GOV2", '
                   '"legalAddress": {"id": "Addr_2", "text": "line2, city2, district2, state2, postal_code2, Denmark", "line": "line2", "city": "city2", "district": "district2", "state": "state2", "postalCode": "postal_code2", '
                     '"country": {"id": "Code_5", "code": "DNK", "codeSystem": "ISO 3166 1 alpha3", "codeSystemVersion": "2020-08", "decode": "Denmark", "instanceType": "Code"}, '
                     '"instanceType": "Address"}, '
                   '"instanceType": "Organization"}, '
                '"instanceType": "ReferenceIdentifier", '
                '"type": {"id": "Code_6", "code": "C142424", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Clinical Development Plan", "instanceType": "Code"}}'
  )
  expected = [expected_1, expected_2]
  ids = ['Code_1', 'Addr_1', 'Code_2', 'Org_1', 'Code_3', 'RI_1', 'Code_4', 'Addr_2', 'Code_5', 'Org_2', 'Code_6', 'RI_2']
  data = [
    [ 'USGOV',  'CT-GOV',  'ClinicalTrials.gov',  'CT.gov Study Registry', 'Study Registry', 'NCT12345678', 'line|district|city|state|postal_code|GBR', 'Pediatric Investigation Plan'],
    [ 'USGOV2', 'CT-GOV2', 'ClinicalTrials2.gov', 'CT.gov Registry',       'Study Registry', 'NCT12345679', 'line2,district2,city2,state2,postal_code2,FRA', 'Clinical Development Plan']
  ]
  sheet = _setup(mocker, globals, data, ids)
  assert len(sheet.items) == 2
  assert sheet.items[0].to_json() == expected[0]
  assert sheet.items[1].to_json() == expected[1]
    
def test_create_empty(mocker, globals):
  ids = []
  data = []
  sheet = _setup(mocker, globals, data, ids)
  assert len(sheet.items) == 0

def test_error(mocker, globals):
  ids = ['Code_1', 'Addr_1', 'Code_2', 'Org_1', 'Code_3', 'RI_1']
  data = {'organisationIdentifierScheme': ['USGOV'], 'organisationIdentifier': ['CT-GOV'], 'organisationName': [''], 'organisationType': ['Study Registry'], 'studyIdentifier': ['NCT12345678'], 'organisationAddress': ['line|district|city|state|postal_code|GBR']}
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  sheet = _setup(mocker, globals, data, ids, MISSING_COLUMN)
  assert sheet.items == []
  assert mock_error.call_count == 3
  errors = [
    mocker.call('studyReferences', 1, 5, 'Empty cell detected where CDISC CT value expected.', 40),
    mocker.call('studyReferences', 1, 7, "Address '' does not contain the required fields (first line, district, city, state, postal code and country code) using ',' separator characters, only 0 found", 40),
    mocker.call('studyReferences', None, None, 'Exception. Failed to create Organization object. See log for additional details.', 40)
  ]
  mock_error.assert_has_calls(errors)
  
def _setup(mocker, globals, data, ids, columns=DEFAULT_COLUMNS):
  globals.cross_references.clear()
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect = ids
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=columns)
  mock_json = mocker.patch("json.load")
  mock_json.return_value = {}
  return StudyReferencesSheet("", globals)
