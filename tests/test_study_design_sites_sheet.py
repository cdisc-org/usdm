import pandas as pd
from usdm_excel.study_design_sites_sheet.study_design_sites_sheet import StudyDesignSitesSheet
from usdm_model.code import Code


def test_create(mocker, globals):
  globals.cross_references.clear()
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Site_1', 'Org_1', 'Addr_1', 'Id_1', 'Site_2', 'Org_2', 'Addr_2', 'Id_2', 'Site_3', 'Org_3', 'Addr_3', 'Id_3']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    [ 'CRO1', 'CRO One',   'Study Registry', 'DUNS', '111111111', 'line|district|city|state|postal_code|GBR',      'Site1', 'Site One', 'Big Site', 'GBR' ],
    [ 'CRO2', 'CRO Two',   'Study Registry', 'DUNS', '222222222', 'line2,district2,city2,state2,postal_code2,FRA', 'Site2', 'Site Two', 'Little Site', 'FRA'],
    [ 'CRO3', 'CRO Three', 'Study Registry', 'DUNS', '333333333', 'line3,district3,city3,state3,postal_code3,FR',  'Site3', 'Site Three', 'Middle Site', '']
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['name', 'label', 'type', 'identifierScheme', 'identifier', 'address', 'siteName', 'siteLabel', 'siteDescription', 'siteCountry'])
  mock_json = mocker.patch("json.load")
  mock_json.return_value = {}
  expected_1 = Code(id='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="GBR")
  expected_2 = Code(id='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="GBR")
  expected_3 = Code(id='Code2', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
  expected_4 = Code(id='Code2', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
  expected_5 = Code(id='Code3', code='code', codeSystem='codesys', codeSystemVersion='3', decode="FRA")
  expected_6 = Code(id='Code2', code='code', codeSystem='codesys', codeSystemVersion='3', decode="GER")
  mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
  mock_code.side_effect=[expected_1, expected_2, expected_3, expected_4, expected_5, expected_6]
  sheet = StudyDesignSitesSheet("", globals)
  assert len(sheet.organizations) == 3
  assert len(sheet.sites) == 3
  assert sheet.organizations[0].model_dump() == {
    'id': 'Id_1',
    'identifier': '111111111',
    'identifierScheme': 'DUNS',
    'instanceType': 'Organization',
    'label': 'CRO One',
    'legalAddress': {
        'city': 'city',
        'country': {
            'code': 'code',
            'codeSystem': 'codesys',
            'codeSystemVersion': '3',
            'decode': 'GBR',
            'id': 'Code1',
            'instanceType': 'Code',
        },
        'district': 'district',
        'id': 'Addr_1',
        'instanceType': 'Address',
        'lines': [
            'line',
        ],
        'postalCode': 'postal_code',
        'state': 'state',
        'text': 'line, city, district, state, postal_code, GBR',
    },
    'managedSites': [
      {
        'country': {
          'code': 'code',
          'codeSystem': 'codesys',
          'codeSystemVersion': '3',
          'decode': 'GBR',
          'id': 'Code1',
          'instanceType': 'Code',
        },
        'description': 'Big Site',
        'id': 'Site_1',
        'instanceType': 'StudySite',
        'label': 'Site One',
        'name': 'Site1',
      },
    ],
    'name': 'CRO1',
    'type': {
      'code': 'C93453',
      'codeSystem': 'http://www.cdisc.org',
      'codeSystemVersion': '2023-12-15',
      'decode': 'Study Registry',
      'id': 'Org_1',
      'instanceType': 'Code',
    }
  }
  assert sheet.organizations[1].model_dump() == {
    'id': 'Id_2',
    'identifier': '222222222',
    'identifierScheme': 'DUNS',
    'instanceType': 'Organization',
    'label': 'CRO Two',
    'legalAddress': {
        'city': 'city2',
        'country': {
            'code': 'code',
            'codeSystem': 'codesys',
            'codeSystemVersion': '3',
            'decode': 'FRA',
            'id': 'Code2',
            'instanceType': 'Code',
        },
        'district': 'district2',
        'id': 'Addr_2',
        'instanceType': 'Address',
        'lines': [
            'line2',
        ],
        'postalCode': 'postal_code2',
        'state': 'state2',
        'text': 'line2, city2, district2, state2, postal_code2, FRA',
    },
    'managedSites': [
      {
        'country': {
          'code': 'code',
          'codeSystem': 'codesys',
          'codeSystemVersion': '3',
          'decode': 'FRA',
          'id': 'Code2',
          'instanceType': 'Code',
        },
        'description': 'Little Site',
        'id': 'Site_2',
        'instanceType': 'StudySite',
        'label': 'Site Two',
        'name': 'Site2',
      },
    ],
    'name': 'CRO2',
    'type': {
      'code': 'C93453',
      'codeSystem': 'http://www.cdisc.org',
      'codeSystemVersion': '2023-12-15',
      'decode': 'Study Registry',
      'id': 'Org_2',
      'instanceType': 'Code',
    }
  }
  
def test_create_empty(mocker, globals):
  globals.cross_references.clear()
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyIdentifierName', 'studyIdentifierDescription', 'studyIdentifierType'])
  sites = StudyDesignSitesSheet("", globals)
  assert len(sites.organizations) == 0

def test_read_cell_by_name_error(mocker, globals):
  globals.cross_references.clear()
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    [ 'CRO1', 'CRO One', 'DUNS', '111111111', 'line|district|city|state|postal_code|GBR', 'Site1', 'Site One', 'Big Site', '' ],
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['name', 'label', 'identifierScheme', 'identifier', 'address', 'siteName', 'siteLabel', 'siteDescription', 'siteCountry'])
  mock_json = mocker.patch("json.load")
  mock_json.return_value = {}
  sites = StudyDesignSitesSheet("", globals)
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyDesignSites"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "Exception. Error [Failed to detect column(s) 'type' in sheet] while reading sheet 'studyDesignSites'. See log for additional details."
