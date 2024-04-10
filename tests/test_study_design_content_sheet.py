import pytest
import pandas as pd
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_design_content_sheet.study_design_content_sheet import StudyDesignContentSheet
from usdm_excel.option_manager import Options, EmptyNoneOption
from tests.test_factory import Factory

xfail = pytest.mark.xfail

def test_create(mocker, globals):
  globals.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.EMPTY)

  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Content_1', 'Content_2', 'Content_3', 'Content_4', 'Content_5', 'Content_6', 'Content_7', 'Content_8']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['1',     '',         'Section 1',     'Text 1'], 
    ['1.1',   'SET NAME', 'Section 1.1',   'Text 1.1'], 
    ['1.2',   '',         'Section 1.2',   'Text 1.2'], 
    ['1.2.1', '',         'Section 1.2.1', 'Text 1.2.1'], 
    ['2',     '',         'Section 2',     'Text 2'], 
    ['2.1',   '',         'Section 2.1',   'Text 2.1'], 
    ['3',     '',         'Section 3',     'Text 3'], 
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber', 'name', 'sectionTitle', 'text'])
  content = StudyDesignContentSheet("", globals)
  assert len(content.items) == 8
  assert content.items[0].name == 'ROOT'
  assert content.items[0].previousId == ''
  assert content.items[0].nextId == 'Content_2'  
  assert content.items[1].id == 'Content_2'
  assert content.items[1].name == 'SECTION 1'
  assert content.items[1].sectionNumber == '1'
  assert content.items[1].sectionTitle == 'Section 1'
  assert content.items[1].text == '<div>Text 1</div>'
  assert content.items[1].childIds == ['Content_3', 'Content_4']
  assert content.items[1].previousId == 'Content_1'
  assert content.items[1].nextId == 'Content_3'  
  assert content.items[2].name == 'SET NAME'
  assert content.items[2].previousId == 'Content_2'
  assert content.items[2].nextId == 'Content_4'  
  assert content.items[3].name == 'SECTION 1.2'
  assert content.items[3].previousId == 'Content_3'
  assert content.items[3].nextId == 'Content_5'  
  assert content.items[4].name == 'SECTION 1.2.1'
  assert content.items[5].name == 'SECTION 2'
  assert content.items[6].name == 'SECTION 2.1'
  assert content.items[7].id == 'Content_8'
  assert content.items[7].name == 'SECTION 3'

def test_create_training_dot(mocker, globals):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Content_1', 'Content_2', 'Content_3', 'Content_4', 'Content_5', 'Content_6', 'Content_7', 'Content_8']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['1',     '',         'Section 1',     'Text 1'], 
    ['1.1',   'SET NAME', 'Section 1.1',   'Text 1.1'], 
    ['1.2',   '',         'Section 1.2',   'Text 1.2'], 
    ['1.2.1', '',         'Section 1.2.1', 'Text 1.2.1.'], 
    ['2',     '',         'Section 2',     'Text 2'], 
    ['2.1',   '',         'Section 2.1',   'Text 2.1.'], 
    ['3',     '',         'Section 3',     'Text 3'], 
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber', 'name', 'sectionTitle', 'text'])
  content = StudyDesignContentSheet("", globals)
  assert len(content.items) == 8
  assert content.items[0].name == 'ROOT'
  assert content.items[1].id == 'Content_2'
  assert content.items[1].name == 'SECTION 1'
  assert content.items[1].sectionNumber == '1'
  assert content.items[1].sectionTitle == 'Section 1'
  assert content.items[1].text == '<div>Text 1</div>'
  assert content.items[1].childIds == ['Content_3', 'Content_4']
  assert content.items[2].name == 'SET NAME'
  assert content.items[3].name == 'SECTION 1.2'
  assert content.items[4].name == 'SECTION 1.2.1'
  assert content.items[5].name == 'SECTION 2'
  assert content.items[6].name == 'SECTION 2.1'
  assert content.items[7].id == 'Content_8'
  assert content.items[7].name == 'SECTION 3'

def test_create_4_levels(mocker, globals):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Content_1', 'Content_2', 'Content_3', 'Content_4', 'Content_5', 'Content_6', 'Content_7', 'Content_8']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['1',       '',         'Section 1',       'Text 1'], 
    ['1.1',     'SET NAME', 'Section 1.1',     'Text 1.1'], 
    ['1.2',     '',         'Section 1.2',     'Text 1.2'], 
    ['1.2.1',   '',         'Section 1.2.1',   'Text 1.2.1'], 
    ['1.2.1.1', '',         'Section 1.2.1.1', 'Text 1.2.1.1'], 
    ['2',       '',         'Section 2',       'Text 2'], 
    ['3',       '',         'Section 3',       'Text 3'], 
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber', 'name', 'sectionTitle', 'text'])
  content = StudyDesignContentSheet("", globals)
  assert len(content.items) == 8
  assert content.items[0].name == 'ROOT'
  assert content.items[4].id == 'Content_5'
  assert content.items[4].name == 'SECTION 1.2.1'
  assert content.items[4].sectionNumber == '1.2.1'
  assert content.items[4].sectionTitle == 'Section 1.2.1'
  assert content.items[4].text == '<div>Text 1.2.1</div>'
  assert content.items[4].childIds == ['Content_6']
  assert content.items[5].id == 'Content_6'
  assert content.items[5].name == 'SECTION 1.2.1.1'
  assert content.items[5].sectionNumber == '1.2.1.1'
  assert content.items[5].sectionTitle == 'Section 1.2.1.1'
  assert content.items[5].text == '<div>Text 1.2.1.1</div>'
  assert content.items[5].childIds == []

def test_create_standard_section(mocker, globals):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Content_1', 'Content_2', 'Content_3', 'Content_4', 'Content_5', 'Content_6', 'Content_7', 'Content_8']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['1',       '',         'Section 1',       'Text 1'], 
    ['1.1',     'SET NAME', 'Section 1.1',     'Text 1.1'], 
    ['1.2',     '',         'Section 1.2',     '<usdm:section name="m11-title">'], 
    ['1.2.1',   '',         'Section 1.2.1',   '<div><usdm:section name="m11-title"></div>'], 
    ['2',       '',         'Section 2',       'Text 2'], 
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber', 'name', 'sectionTitle', 'text'])
  content = StudyDesignContentSheet("", globals)
  assert len(content.items) == 6
  assert content.items[0].text == ''
  assert content.items[1].text == '<div>Text 1</div>'
  assert content.items[2].text == '<div>Text 1.1</div>'
  assert content.items[3].text == '<div><usdm:section name="m11-title"></div>'
  assert content.items[4].text == '<div><usdm:section name="m11-title"></div>'
  assert content.items[5].text == '<div>Text 2</div>'

def test_create_invalid_levels(mocker, globals):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Content_1', 'Content_2', 'Content_3', 'Content_4', 'Content_5', 'Content_6', 'Content_7', 'Content_8']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['1',         '',         'Section 1',       'Text 1'], 
    ['1.1',       'SET NAME', 'Section 1.1',     'Text 1.1'], 
    ['1.2',       '',         'Section 1.2',     'Text 1.2'], 
    ['1.2.1',     '',         'Section 1.2.1',   'Text 1.2.1'], 
    ['1.2.1.1.4', '',         'Section 1.2.1.1', 'Text 1.2.1.1'], 
    ['2',         '',         'Section 2',       'Text 2'], 
    ['3',         '',         'Section 3',       'Text 3'], 
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber', 'name', 'sectionTitle', 'text'])
  StudyDesignContentSheet("", globals)
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyDesignContent"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "Exception '' raised reading sheet 'studyDesignContent'"

def test_create_empty(mocker, globals):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber', 'name', 'sectionTitle', 'text'])
  content = StudyDesignContentSheet("", globals)
  assert len(content.items) == 1

def test_read_cell_by_name_error(mocker, globals):
  
  call_parameters = []
  
  def my_add(sheet, row, column, message, level=10):
    call_parameters.append((sheet, row, column, message, level))
    return None

  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add", side_effect=my_add)
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['1', 'Section 1', 'Text 1']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber', 'name', 'text'])
  content = StudyDesignContentSheet("", globals)
  mock_error.assert_called()
  assert call_parameters == [
    ('studyDesignContent', 1, -1, "Error 'Failed to detect column(s) 'sectionTitle' in sheet' reading cell 'sectionTitle'", 10)
  ]
  