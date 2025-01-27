import pandas as pd
from usdm_excel.study_identifier_and_organization_sheets.study_organisations_sheet import StudyOrganizationsSheet
from usdm_excel.base_sheet import BaseSheet
from usdm_model.code import Code

def test_success(mocker, globals):
  ids = ['Code_1', 'Addr_1', 'Code_2', 'Org_1']
  expected = ( '{"id": "Org_1", "name": "ClinicalTrials.gov", "label": "", '
               '"type": {"id": "Code_1", "code": "C93453", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Study Registry", "instanceType": "Code"}, '
               '"identifierScheme": "USGOV", "identifier": "CT-GOV", '
               '"legalAddress": {"id": "Addr_1", "text": "line, city, district, state, postal_code, Denmark", "lines": ["line"], "city": "city", "district": "district", "state": "state", "postalCode": "postal_code", '
                 '"country": {"id": "Code_2", "code": "DNK", "codeSystem": "ISO 3166 1 alpha3", "codeSystemVersion": "2020-08", "decode": "Denmark", "instanceType": "Code"}, '
                 '"instanceType": "Address"}, '
               '"managedSites": [], '
               '"instanceType": "Organization"}'
  )
  data = {'organisationIdentifierScheme': ['USGOV'], 'organisationIdentifier': ['CT-GOV'], 'organisationName': ['ClinicalTrials.gov'], 'organisationType': ['Study Registry'], 'studyIdentifier': ['NCT12345678'], 'organisationAddress': ['line|district|city|state|postal_code|GBR']}
  item = _setup_base(mocker, globals, data, ids)
  assert len(item.items) == 1
  assert str(item.items[0].to_json()) == expected

def test_no_address(mocker, globals):
  ids = ['Code_1', 'Org_1']
  expected = ( '{"id": "Org_1", "name": "ClinicalTrials.gov", "label": "", '
               '"type": {"id": "Code_1", "code": "C93453", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Study Registry", "instanceType": "Code"}, '
               '"identifierScheme": "USGOV", "identifier": "CT-GOV", '
               '"legalAddress": null, '
               '"managedSites": [], '
               '"instanceType": "Organization"}'
  )
  data = {'organisationIdentifierScheme': ['USGOV'], 'organisationIdentifier': ['CT-GOV'], 'organisationName': ['ClinicalTrials.gov'], 'organisationType': ['Study Registry'], 'studyIdentifier': ['NCT12345678'], 'organisationAddress': ['']}
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  item = _setup_base(mocker, globals, data, ids)
  assert len(item.items) == 1
  assert str(item.items[0].to_json()) == expected
  assert mock_error.call_count == 1
  mock_error.assert_has_calls([mocker.call('studyOrganizations', 1, 6, "Address '' does not contain the required fields (lines, district, city, state, postal code and country code) using ',' separator characters, only 0 found", 40)])

def test_organization_error(mocker, globals):
  ids = ['Code_1', 'Addr_1', 'Code_2', 'Org_1']
  data = {'organisationIdentifierScheme': ['USGOV'], 'organisationIdentifier': ['CT-GOV'], 'organisationName': [''], 'organisationType': ['Study Registry'], 'studyIdentifier': ['NCT12345678'], 'organisationAddress': ['line|district|city|state|postal_code|GBR']}
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  item = _setup_base(mocker, globals, data, ids)
  assert len(item.items) == 0
  assert mock_error.call_count == 1
  mock_error.assert_has_calls([mocker.call('studyOrganizations', None, None, 'Exception. Failed to create Organization object. See log for additional details.', 40)])

def _setup_base(mocker, globals, data, ids):
  globals.cross_references.clear()
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=ids
  mock_json = mocker.patch("json.load")
  mock_json.return_value = {}
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame.from_dict(data)
  return StudyOrganizationsSheet("", globals)
  