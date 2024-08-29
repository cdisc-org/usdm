import pandas as pd
from usdm_excel.study_identifiers_sheet.organization import get_organization
from usdm_excel.base_sheet import BaseSheet
from usdm_model.code import Code

def test_success(mocker, globals):
  ids = ['Code_1', 'Addr_1', 'Code_2', 'Org_1']
  expected = ( '{"id": "Org_1", "name": "ClinicalTrials.gov", "label": "", '
               '"organizationType": {"id": "Code_1", "code": "C93453", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Study Registry", "instanceType": "Code"}, '
               '"identifierScheme": "USGOV", "identifier": "CT-GOV", '
               '"legalAddress": {"id": "Addr_1", "text": "line, city, district, state, postal_code, Denmark", "line": "line", "city": "city", "district": "district", "state": "state", "postalCode": "postal_code", '
                 '"country": {"id": "Code_2", "code": "DNK", "codeSystem": "ISO 3166 1 alpha3", "codeSystemVersion": "2020-08", "decode": "Denmark", "instanceType": "Code"}, '
                 '"instanceType": "Address"}, '
               '"instanceType": "Organization"}'
  )
  data = {'organisationIdentifierScheme': ['USGOV'], 'organisationIdentifier': ['CT-GOV'], 'organisationName': ['ClinicalTrials.gov'], 'organisationType': ['Study Registry'], 'studyIdentifier': ['NCT12345678'], 'organisationAddress': ['line|district|city|state|postal_code|GBR']}
  base = _setup_base(mocker, globals, data, ids)
  item = get_organization(base, 0)
  assert str(item.to_json()) == expected

def test_no_address(mocker, globals):
  ids = ['Code_1', 'Org_1']
  expected = ( '{"id": "Org_1", "name": "ClinicalTrials.gov", "label": "", '
               '"organizationType": {"id": "Code_1", "code": "C93453", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Study Registry", "instanceType": "Code"}, '
               '"identifierScheme": "USGOV", "identifier": "CT-GOV", '
               '"legalAddress": null, '
               '"instanceType": "Organization"}'
  )
  data = {'organisationIdentifierScheme': ['USGOV'], 'organisationIdentifier': ['CT-GOV'], 'organisationName': ['ClinicalTrials.gov'], 'organisationType': ['Study Registry'], 'studyIdentifier': ['NCT12345678'], 'organisationAddress': ['']}
  base = _setup_base(mocker, globals, data, ids)
  item = get_organization(base, 0)
  assert str(item.to_json()) == expected

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
  base = BaseSheet("", globals, "sheet")
  return base