import pytest
import pandas as pd

xfail = pytest.mark.xfail

from usdm_excel.study_design_eligibility_criteria_sheet.study_design_eligibility_criteria_sheet import StudyDesignEligibilityCriteriaSheet
from usdm_model.code import Code

def test_create(mocker):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Code_1', 'EligibilityId_1', 'Code_2', 'EligibilityId_2', 'Code_3', 'EligibilityId_3']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['Inclusion', '01', 'INC01', 'The study age criterion', 'Age critierion', 'Subjects should be between 18 and 45 years old', "dictionary"], 
    ['Inclusion', '02', 'INC01', 'The study abc criterion',   'ABC critierion', 'Subjects should have ABC', "dictionary"], 
    ['Exclusion', '01', 'EXC01', 'Exclude those with all fingers',   'Fingers critierion', 'Subjects should not have all fingers', "dictionary"], 
 ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['category', 'identifier', 'name', 'description', 'label', 'text', 'dictionary'])
  items = StudyDesignEligibilityCriteriaSheet("")
  assert len(items.items) == 3
  assert items.items[0].id == 'EligibilityId_1'
  assert items.items[0].category.decode == 'Inclusion Criteria'
  assert items.items[0].identifier == '01'
  assert items.items[0].name == 'INC01'
  assert items.items[0].description == 'The study age criterion'
  assert items.items[0].label == 'Age critierion'
  assert items.items[0].text == 'Subjects should be between 18 and 45 years old'
  assert items.items[1].category.decode == 'Inclusion Criteria'
  assert items.items[2].category.decode == 'Exclusion Criteria'
  
def test_create_empty(mocker):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['category', 'identifier', 'name', 'description', 'label', 'text', 'dictionary'])
  items = StudyDesignEligibilityCriteriaSheet("")
  assert len(items.items) == 0

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
    ['Inclusion', '01', 'The study age criterion', 'Age critierion', 'Subjects should be between 18 and 45 years old', "dictionary"]
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['category', 'identifier', 'name', 'label', 'text', 'dictionary'])
  items = StudyDesignEligibilityCriteriaSheet("")
  mock_error.assert_called()
  assert call_parameters == [
    ('studyDesignEligibilityCriteria', 1, -1, "Error 'Failed to detect column(s) 'description' in sheet' reading cell 'description'", 10),
    ('studyDesignEligibilityCriteria', 1, 5, "Dictionary 'dictionary' not found", 30),
    ('studyDesignEligibilityCriteria', None, None, "Unable to find dictionary with name 'dictionary'", 10)
  ]
  
