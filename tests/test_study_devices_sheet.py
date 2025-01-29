from tests.mocks.mock_general import *
from tests.mocks.mock_sheet import *
from tests.mocks.mock_ids import *
from tests.mocks.mock_logging import *
from usdm_excel.study_devices_sheet.study_devices_sheet import StudyDevicesSheet
from usdm_excel.option_manager import Options, EmptyNoneOption
from tests.test_factory import Factory
from usdm_model.administrable_product import AdministrableProduct
from usdm_model.code import Code
def test_create(mocker, globals):
  globals.id_manager.clear()
  globals.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.NONE.value)
  organizations(globals)
  sheet_data = {
    'name': ['DEVICE1', 'DEVICE2'], 
    'description': ['DESCRIPTION1', 'DESCRIPTION2'], 
    'label': ['LABEL1', 'LABEL2'],
    'hardwareVersion': ['HARDWAREVERSION1', 'HARDWAREVERSION2'],
    'softwareVersion': ['SOFTWAREVERSION1', 'SOFTWAREVERSION2'],
    'sourcing': ['Centrally Sourced', 'Locally Sourced'],
    'product': ['PRODUCT1', 'PRODUCT2'],
    'notes': ['', ''],
  }
  mock_sheet_present(mocker)
  mock_sheet(mocker, globals, sheet_data)
  mock_json = mocker.patch("json.load")
  mock_json.side_effect=[{}, {}]
  expected_1 = Code(id='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="Centrally Sourced")
  expected_2 = Code(id='Code2', code='code', codeSystem='codesys', codeSystemVersion='3', decode="Locally Sourced")
  mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
  mock_code.side_effect=[expected_1, expected_2]
  item = StudyDevicesSheet("", globals)
  assert len(item.items) == 2
  assert item.items[0].model_dump() == {
    'id': 'MedicalDevice_1',
    'instanceType': 'MedicalDevice',
    'name': 'DEVICE1',
    'label': 'LABEL1',
    'description': 'DESCRIPTION1',
    'hardwareVersion': 'HARDWAREVERSION1',
    'softwareVersion': 'SOFTWAREVERSION1',
    'embeddedProductId': None,
    'identifiers': [],
    'sourcing': {
      'code': 'code',
      'codeSystem': 'codesys',
      'codeSystemVersion': '3',
      'decode': 'Centrally Sourced',
      'id': 'Code1',
      'instanceType': 'Code',
    },
    'notes': [],
  }
  assert item.items[1].model_dump() == {
    'id': 'MedicalDevice_2',
    'instanceType': 'MedicalDevice',
    'name': 'DEVICE2',
    'label': 'LABEL2',
    'description': 'DESCRIPTION2',
    'hardwareVersion': 'HARDWAREVERSION2',
    'softwareVersion': 'SOFTWAREVERSION2',
    'embeddedProductId': None,
    'identifiers': [],
    'sourcing': {
      'code': 'code',
      'codeSystem': 'codesys',
      'codeSystemVersion': '3',
      'decode': 'Locally Sourced',
      'id': 'Code2',
      'instanceType': 'Code',
    },
    'notes': [],
  }

def test_create_empty(mocker, globals):
  sheet_data = {}
  mock_sheet_present(mocker)
  mock_sheet(mocker, globals, sheet_data)
  item = StudyDevicesSheet("", globals)
  assert len(item.items) == 0

def test_read_cell_by_name_error(mocker, globals):
  sheet_data = {
    'name': ['DEVICE1'], 
    'description': ['DESCRIPTION1'], 
    'label': ['LABEL1'],
    'softwareVersion': ['SOFTWAREVERSION1'],
    'hardwareVersion': ['HARDWAREVERSION1'],
    'product': ['PRODUCT1'],
    'notes': [''],
  }
  mea = mock_error_add(mocker, [None, None, None, None, None, None])
  mock_sheet_present(mocker)
  expected_1 = Code(id='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="Centrally Sourced")
  mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
  mock_code.side_effect=[expected_1]
  mock_sheet(mocker, globals, sheet_data)
  item = StudyDevicesSheet("", globals)
  assert mock_called(mea, 1)
  mock_parameters_correct(mea, [mocker.call('studyDevices', None, None, "Exception. Error [Failed to detect column(s) 'sourcing' in sheet] while reading sheet 'studyDevices'. See log for additional details.", 40)])

def organizations(globals):
  factory = Factory(globals)
  dose_code = factory.cdisc_code("C12345", "something_dose")
  prod1 = factory.item(AdministrableProduct, {'name': 'PRODUCT1', 'productDesignation': factory.cdisc_code("C6789", "designation"), 'administrableDoseForm': factory.alias_code(dose_code, alias_codes=[])}) 
  prod2 = factory.item(AdministrableProduct, {'name': 'PRODUCT2', 'productDesignation': factory.cdisc_code("C6789", "designation"), 'administrableDoseForm': factory.alias_code(dose_code, alias_codes=[])}) 
  prod3 = factory.item(AdministrableProduct, {'name': 'PRODUCT3', 'productDesignation': factory.cdisc_code("C6789", "designation"), 'administrableDoseForm': factory.alias_code(dose_code, alias_codes=[])}) 
  globals.cross_references.add(prod1.name, prod1)
  globals.cross_references.add(prod2.name, prod2)
  globals.cross_references.add(prod3.name, prod3)  
