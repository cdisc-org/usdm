import pytest
import pandas as pd

from src.usdm_excel.base_sheet import BaseSheet

xfail = pytest.mark.xfail

from usdm_excel.study_design_content_sheet.study_design_content_sheet import StudyDesignContentSheet

def test_create(mocker):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
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
  content = StudyDesignContentSheet("")
  assert len(content.items) == 8
  assert content.items[0].name == 'ROOT'
  assert content.items[1].id == 'Content_2'
  assert content.items[1].name == 'SECTION 1'
  assert content.items[1].sectionNumber == '1'
  assert content.items[1].sectionTitle == 'Section 1'
  assert content.items[1].text == 'Text 1'
  assert content.items[1].contentChildIds == ['Content_3', 'Content_4']
  assert content.items[2].name == 'SET NAME'
  assert content.items[3].name == 'SECTION 1.2'
  assert content.items[4].name == 'SECTION 1.2.1'
  assert content.items[5].name == 'SECTION 2'
  assert content.items[6].name == 'SECTION 2.1'
  assert content.items[7].id == 'Content_8'
  assert content.items[7].name == 'SECTION 3'
  
def test_create_4_levels(mocker):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
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
  content = StudyDesignContentSheet("")
  assert len(content.items) == 8
  assert content.items[0].name == 'ROOT'
  assert content.items[4].id == 'Content_5'
  assert content.items[4].name == 'SECTION 1.2.1'
  assert content.items[4].sectionNumber == '1.2.1'
  assert content.items[4].sectionTitle == 'Section 1.2.1'
  assert content.items[4].text == 'Text 1.2.1'
  assert content.items[4].contentChildIds == ['Content_6']
  assert content.items[5].id == 'Content_6'
  assert content.items[5].name == 'SECTION 1.2.1.1'
  assert content.items[5].sectionNumber == '1.2.1.1'
  assert content.items[5].sectionTitle == 'Section 1.2.1.1'
  assert content.items[5].text == 'Text 1.2.1.1'
  assert content.items[5].contentChildIds == []

def test_create_invalid_levels(mocker):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
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
  StudyDesignContentSheet("")
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyDesignContent"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "Exception [] raised reading sheet."

def test_create_empty(mocker):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber', 'name', 'sectionTitle', 'text'])
  content = StudyDesignContentSheet("")
  assert len(content.items) == 1

def test_read_cell_by_name_error(mocker):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['1', 'Section 1', 'Text 1']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber', 'sectionTitle', 'text'])
  content = StudyDesignContentSheet("")
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyDesignContent"
  assert mock_error.call_args[0][1] == 1
  assert mock_error.call_args[0][2] == -1
  assert mock_error.call_args[0][3] == "Error reading cell 'name'"
  
