import pandas as pd
from usdm_excel.study_identifiers_sheet.study_references_sheet import StudyReferencesSheet
from usdm_model.code import Code

DEFAULT_COLUMNS = ['IdentifierScheme', 'organisationIdentifier', 'name', 'label', 'type', 'studyIdentifier', 'address', 'referenceType']
MISSING_COLUMN =  ['IdentifierScheme', 'organisationIdentifier', 'name', 'label', 'type', 'studyIdentifier', 'address']

def test_create(mocker, globals):
  expected_1 = ('{"id": "Org_1", "name": "ClinicalTrials.gov", "label": "", '
                 '"organizationType": {"id": "Code_1", "code": "C93453", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Study Registry", "instanceType": "Code"}, '
                 '"identifierScheme": "USGOV", "identifier": "CT-GOV", '
                 '"legalAddress": {"id": "Addr_1", "text": "line, city, district, state, postal_code, Denmark", "line": "line", "city": "city", "district": "district", "state": "state", "postalCode": "postal_code", '
                   '"country": {"id": "Code_2", "code": "DNK", "codeSystem": "ISO 3166 1 alpha3", "codeSystemVersion": "2020-08", "decode": "Denmark", "instanceType": "Code"}, '
                   '"instanceType": "Address"}, '
                 '"instanceType": "Organization"}'
  )
  expected_2 = ('{"id": "Org_1", "name": "ClinicalTrials.gov", "label": "", '
                   '"organizationType": {"id": "Code_1", "code": "C93453", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Study Registry", "instanceType": "Code"}, '
                   '"identifierScheme": "USGOV", "identifier": "CT-GOV", '
                   '"legalAddress": {"id": "Addr_1", "text": "line, city, district, state, postal_code, Denmark", "line": "line", "city": "city", "district": "district", "state": "state", "postalCode": "postal_code", '
                     '"country": {"id": "Code_2", "code": "DNK", "codeSystem": "ISO 3166 1 alpha3", "codeSystemVersion": "2020-08", "decode": "Denmark", "instanceType": "Code"}, '
                     '"instanceType": "Address"}, '
                   '"instanceType": "Organization"}'
  )
  expected = [expected_1, expected_2]
  ids = ['Code_1', 'Code_2', 'Addr_1', 'Id_1', 'Code_3', 'Org_1', 'Org_2', 'Addr_2', 'Id_2', 'Code_3', 'Org_3', 'Addr_3', 'Id_3']
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
  ids = ['Code_1', 'Addr_1', 'Code_2', 'Org_1']
  data = {'organisationIdentifierScheme': ['USGOV'], 'organisationIdentifier': ['CT-GOV'], 'organisationName': [''], 'organisationType': ['Study Registry'], 'studyIdentifier': ['NCT12345678'], 'organisationAddress': ['line|district|city|state|postal_code|GBR']}
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  sheet = _setup(mocker, globals, data, ids, MISSING_COLUMN)
  assert sheet.items == []
  assert mock_error.call_count == 1
  mock_error.assert_has_calls([mocker.call('sheet', None, None, 'Exception. Failed to create Organization object. See log for additional details.', 40)])
  
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
