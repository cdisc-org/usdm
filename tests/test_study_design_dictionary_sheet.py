import pytest
import pandas as pd

xfail = pytest.mark.xfail

from usdm_excel.study_design_dictionary_sheet.study_design_dictionary_sheet import StudyDesignDictionarySheet
from usdm_model.api_base_model import ApiBaseModelWithId

def test_create(mocker):
  mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
  mock_cross_ref.side_effect=[ApiBaseModelWithId(id="1"), ApiBaseModelWithId(id="2"), ApiBaseModelWithId(id="3"), ApiBaseModelWithId(id="4"), ApiBaseModelWithId(id="5")]
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['DictionaryId_1', 'DictionaryId_2', 'DictionaryId_3']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['Dictionary 1', 'Dictionary One',   'Label One',   'Key 1', 'Klass 1', 'Id 1', 'Attribute 1'], 
    ['',             '',                 '',            'Key 2', 'Klass 2', 'Id 2', 'Attribute 2'], 
    ['Dictionary 2', 'Dictionary Two',   'Label Two',   'Key 3', 'Klass 3', 'Id 3', 'Attribute 3'], 
    ['Dictionary 3', 'Dictionary Three', 'Label Three', 'Key 4', 'Klass 4', 'Id 4', 'Attribute 4'], 
    ['',             '',                 '',            'Key 5', 'Klass 5', 'Id 5', 'Attribute 5']
 ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['name', 'description', 'label', 'key', 'class', 'xref', 'attribute'])
  dictionaries = StudyDesignDictionarySheet("")
  assert len(dictionaries.items) == 3
  assert dictionaries.items[0].id == 'DictionaryId_1'
  assert dictionaries.items[0].name == 'Dictionary 1'
  assert dictionaries.items[0].description == 'Dictionary One'
  assert dictionaries.items[0].label == 'Label One'
  assert dictionaries.items[0].parameterMap['Key 2']['klass'] == 'Klass 2'
  assert list(dictionaries.items[1].parameterMap.keys()) == ['Key 3']
  assert list(dictionaries.items[2].parameterMap.keys()) == ['Key 4', 'Key 5']
  
def test_create_empty(mocker):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['name', 'description', 'label', 'key', 'class', 'xref', 'attribute'])
  dictionaries = StudyDesignDictionarySheet("")
  assert len(dictionaries.items) == 0

def test_read_cell_by_name_error(mocker):
  
  call_parameters = []
  
  def my_add(sheet, row, column, message, level=10):
    call_parameters.append((sheet, row, column, message, level))
    return None

  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add", side_effect=my_add)
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['Dictionary 1', 'Dictionary One',   'Label One',   'Key 1', 'Klass 1', 'Attribute 1']
 ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['name', 'description', 'label', 'key', 'class', 'attribute'])
  dictionaries = StudyDesignDictionarySheet("")
  mock_error.assert_called()
  assert call_parameters == [
    ("dictionaries", 1, -1, "Error reading cell 'xref'", 10),
    ('dictionaries', None, None, "Unable to resolve dictionary reference klass: 'Klass 1', name: '', attribute 'Attribute 1'", 30)
  ]
  
