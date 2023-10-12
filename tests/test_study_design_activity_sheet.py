import pytest
import pandas as pd

xfail = pytest.mark.xfail

from usdm_excel.study_design_activity_sheet.study_design_activity_sheet import StudyDesignActivitySheet
from usdm_model.code import Code

def test_create(mocker):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['ActivityId_1', 'ActivityId_2', 'ActivityId_3']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['Activity 1', 'Activity One', '', ''], ['Activity 2', 'Activity Two', 'T', 'Condition 2'], ['Activity 3', 'Activity Three', 'F', '']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['activityName', 'activityDescription', 'activityIsConditional', 'activityIsConditionalReason'])
  activities = StudyDesignActivitySheet("")
  assert len(activities.items) == 3
  assert activities.items[0].id == 'ActivityId_1'
  assert activities.items[0].name == 'Activity 1'
  assert activities.items[0].description == 'Activity One'
  assert activities.items[0].activityIsConditional == False
  assert activities.items[0].activityIsConditionalReason == ''
  assert activities.items[1].id == 'ActivityId_2'
  assert activities.items[1].description == 'Activity Two'
  assert activities.items[1].activityIsConditional == True
  assert activities.items[1].activityIsConditionalReason == 'Condition 2'
  assert activities.items[2].id == 'ActivityId_3'
  assert activities.items[2].activityIsConditional == False
  
def test_create_empty(mocker):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyActivityName', 'studyActivityDescription', 'studyActivityType'])
  activities = StudyDesignActivitySheet("")
  assert len(activities.items) == 0

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
  data = [['Activity 1', 'Activity One']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['activityName', 'activityDescription'])
  activities = StudyDesignActivitySheet("")
  mock_error.assert_called()
  assert call_parameters == [
    ("studyDesignActivities", 1, -1, "Error reading cell 'activityIsConditional'", 10),
    ("studyDesignActivities", 1, -1, "Error reading cell 'activityIsConditionalReason'", 10),
  ]
  
