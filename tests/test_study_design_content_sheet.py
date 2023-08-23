import pytest
import pandas as pd

xfail = pytest.mark.xfail

from src.usdm_excel.study_design_content_sheet.study_design_content_sheet import StudyDesignContentSheet

def test_create(mocker):
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['Content_1', 'Content_2', 'Content_3', 'Content_4', 'Content_5', 'Content_6', 'Content_7']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['1', '',    '',      '',         'Section 1',     'Text 1'], 
    ['',  '1.1', '',      'SET NAME', 'Section 1.1',   'Text 1.1'], 
    ['',  '1.2', '',      '',         'Section 1.2',   'Text 1.2'], 
    ['',  '',    '1.2.1', '',         'Section 1.2.1', 'Text 1.2.1'], 
    ['2', '',    '',      '',         'Section 2',     'Text 2'], 
    ['',  '2.1', '',      '',         'Section 2.1',   'Text 2.1'], 
    ['3', '',    '',      '',         'Section 3',     'Text 3'], 
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber1', 'sectionNumber2', 'sectionNumber3', 'name', 'sectionTitle', 'text'])
  content = StudyDesignContentSheet("")
  assert len(content.items) == 7
  assert content.items[0].id == 'Content_1'
  assert content.items[0].name == 'SECTION 1'
  assert content.items[0].sectionNumber == '1'
  assert content.items[0].sectionTitle == 'Section 1'
  assert content.items[0].text == 'Text 1'
  assert content.items[0].contentChildIds == ['Content_2', 'Content_3']
  
def test_create_empty(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber1', 'sectionNumber2', 'sectionNumber3', 'name', 'sectionTitle', 'text'])
  content = StudyDesignContentSheet("")
  assert len(content.items) == 0

def test_read_cell_by_name_error(mocker):
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['1', '', '', 'Section 1', 'Text 1']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber1', 'sectionNumber2', 'sectionNumber3', 'sectionTitle', 'text'])
  content = StudyDesignContentSheet("")
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyDesignContent"
  assert mock_error.call_args[0][1] == 1
  assert mock_error.call_args[0][2] == -1
  assert mock_error.call_args[0][3] == "Error ('name') reading cell"
  
