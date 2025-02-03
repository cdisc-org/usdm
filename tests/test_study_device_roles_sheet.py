import pandas as pd
from usdm_excel.study_devices_sheet.study_devices_role_sheet import StudyDeviceRoleSheet
from usdm_model.organization import Organization
from usdm_excel.globals import Globals
from tests.test_factory import Factory

def test_create(factory, mocker, globals):
  data = {
    'name': ['AP1', 'AP2', 'AP3'], 
    'description': ['Desc One', 'Desc Two', 'Desc Three'],
    'label': ['Lable 1', 'L2', 'L3'],
    'organization': ['Sponsor 1', 'Sponsor 2', 'Sponsor 3'],
    'role': ['Manufacturer', 'Supplier', 'Supplier']
  }
  expected_1 = ( '{"id": "AP_1", "name": "AP1", "label": "Lable 1", "description": "Desc One", '
                 '"code": {"id": "C_4", "code": "C99915x1", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Manufacturer", "instanceType": "Code"}, '
                 '"appliesToIds": [], "organizationId": "O_1", '
                 '"instanceType": "ProductOrganizationRole"}'
                )
  expected_2 = ( '{"id": "AP_2", "name": "AP2", "label": "L2", "description": "Desc Two", '
                 '"code": {"id": "C_5", "code": "C99915x2", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Supplier", "instanceType": "Code"}, '
                 '"appliesToIds": [], "organizationId": "O_2", '
                 '"instanceType": "ProductOrganizationRole"}'
                )
  expected_3 = ( '{"id": "AP_3", "name": "AP3", "label": "L3", "description": "Desc Three", '
                 '"code": {"id": "C_6", "code": "C99915x2", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Supplier", "instanceType": "Code"}, '
                 '"appliesToIds": [], "organizationId": "O_3", '
                 '"instanceType": "ProductOrganizationRole"}'
                )
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['C_1', 'C_2', 'C_3', 'O_1', 'O_2', 'O_3', 'C_4', 'AP_1', 'C_5', 'AP_2', 'C_6', 'AP_3']
  _setup(mocker, globals, data)
  _create_orgs(factory, globals)
  item = StudyDeviceRoleSheet("", globals)
  assert len(item.items) == 3
  assert item.items[0].to_json() == expected_1
  assert item.items[1].to_json() == expected_2
  assert item.items[2].to_json() == expected_3

def test_create_empty(mocker, globals):
  data = {}
  _setup(mocker, globals, data)
  item = StudyDeviceRoleSheet("", globals)
  assert len(item.items) == 0

def test_read_cell_by_name_error(mocker, globals):
  data = {
    'name': ['AP1'], 
    'description': ['Desc One'],
    'label': ['Lable 1'],
    'role': ['Investigator']
  }
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Code_1', 'Abbreviation_1']
  _setup(mocker, globals, data)
  item = StudyDeviceRoleSheet("", globals)
  assert mock_error.call_count == 2
  mock_error.assert_has_calls(
    [
      mocker.call('deviceRoles', 1, -1, "Error attempting to read cell 'organization'. Exception: Failed to detect column(s) 'organization' in sheet", 40),
      mocker.call('deviceRoles', None, None, "Exception. Error ['NoneType' object has no attribute 'id'] while reading sheet 'deviceRoles'. See log for additional details.", 40)
    ]
  )
  
def _setup(mocker, globals, data):
  globals.cross_references.clear()
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame.from_dict(data)

def _create_orgs(factory: Factory, globals: Globals):
  items = [
    {'name': 'Sponsor 1', 'type': factory.cdisc_code("C70793", "sponsor"), 'identifier': "123456789", 'identifierScheme': "DUNS", 'legalAddress': None},
    {'name': 'Sponsor 2', 'type': factory.cdisc_code("C70793", "sponsor"), 'identifier': "222222222", 'identifierScheme': "DUNS", 'legalAddress': None}, 
    {'name': 'Sponsor 3', 'type': factory.cdisc_code("C70793", "sponsor"), 'identifier': "333333333", 'identifierScheme': "DUNS", 'legalAddress': None}
  ]
  for item in items:
    org = factory.item(Organization, item)
    globals.cross_references.add(item['name'], org)


 