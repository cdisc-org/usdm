import pandas as pd

from usdm_excel.study_design_timing_sheet.study_design_timing_sheet import StudyDesignTimingSheet
from usdm_excel.study_design_timing_sheet.window_type import WindowType

def test_create(mocker):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['Code1', 'Code2', 'TimingId_1', 'Code3', 'Code4', 'TimingId_2', 'Code5', 'Code6', 'TimingId_3']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['Timing 1', 'Timing One', 'T1', 'After', 'X1', 'X2', '3 days', 'S2S', '-1..1 day'],
    ['Timing 2', 'Timing Two', 'T2', 'Before', 'X2', 'X3', '10 days', 'E2S', ''], 
    ['Timing 3', 'Timing Three', 'T3', 'Fixed', 'X4', 'X5', '3 days', 'e2e', '']
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['name', 'description', 'label', 'type', 'from', 'to', 'timingValue', 'toFrom', 'window'])

  

  items = StudyDesignTimingSheet("")
  assert len(items.items) == 3
  assert items.items[0].id == 'TimingId_1'
  assert items.items[0].name == 'Timing 1'
  assert items.items[0].description == 'Timing One'
  assert items.items[0].type.decode == 'After'
  assert items.items[1].id == 'TimingId_2'
  assert items.items[1].description == 'Timing Two'
  assert items.items[1].type.decode == 'Before'
  assert items.items[2].id == 'TimingId_3'
  assert items.items[2].type.decode == 'Fixed Reference'

# def test_timepoint_type(mocker):
#   mocked_open = mocker.mock_open(read_data="File")
#   mocker.patch("builtins.open", mocked_open)
#   mock_read = mocker.patch("pandas.read_excel")
#   data = { 'col_1': [ 'A:', 'P: 2D ', 'P2:2D', 'C:', 'N3: 3 weeks', 'N: +2 days', 'P: -3 hrs' ] }
#   mock_read.return_value = pd.DataFrame.from_dict(data)
#   parent = BaseSheet("", "")
#   test_data = [
#     (0,0,'anchor', 0, None, ISO8601Duration.ZERO_DURATION),
#     (1,0,'previous', -1, "2D", "P2D"),
#     (2,0,'previous', -2, "2D", "P2D"),
#     (3,0,'cycle start', 1, None, ISO8601Duration.ZERO_DURATION),
#     (4,0,'next', 3, "3 weeks", "P3W"),
#     (5,0,'next', 1, "+2 days", "P2D"),
#     (6,0,'previous', -1, "-3 hrs", "PT3H"),
#   ]
#   for index, test in enumerate(test_data):
#     item = TimepointType(parent, test[0], test[1])
#     assert(item.timing_type) == test[2]
#     assert(item.relative_ref) == test[3]
#     assert(item.description) == test[4]
#     assert(item.value) == test[5]

# def test_timepoint_type_error(mocker):
#   mocked_open = mocker.mock_open(read_data="File")
#   mocker.patch("builtins.open", mocked_open)
#   mock_read = mocker.patch("pandas.read_excel")
#   data = { 'col_1': [ 'A', 'P: 2 ', '', 'P2: 2 decades' ] }
#   mock_read.return_value = pd.DataFrame.from_dict(data)
#   parent = BaseSheet("", "Sheet X")
#   test_data = [
#     (0,0,"Could not decode the timing value, no ':' detected in 'A'"),
#     (1,0,"Could not decode the duration value, no value and units found in '2'"),
#     (2,0,"Could not decode the timing value, cell was empty"),
#     (3,0,"Could not decode the duration value '2 decades'"),
#   ]
#   for index, test in enumerate(test_data):
#     mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
#     item = TimepointType(parent, test[0], test[1])
#     mock_error.assert_called()
#     assert mock_error.call_args[0][0] == "Sheet X"
#     assert mock_error.call_args[0][1] == test[0] + 1
#     assert mock_error.call_args[0][2] == test[1] + 1
#     assert mock_error.call_args[0][3] == test[2]

def test_window_type(mocker):
  test_data = [
    ('1..1 Days', "P1D", "P1D", '1..1 Days'),
    (' -1..1 days', "P1D", "P1D", '-1..1 days'),
    ('-1 .. 1 weeks ', "P1W", "P1W", '-1 .. 1 weeks'),
  ]
  for index, test in enumerate(test_data):
    item = WindowType(test[0])
    assert(item.lower) == test[1]
    assert(item.upper) == test[2]
    assert(item.label) == test[3]
    assert(item.errors) == [] 

def test_window_type_error(mocker):
  test_data = [
    ('1.. Days',"Could not decode the window value, not all required parts detected in '1.. Days'"),
    ('-1.1 days',"Could not decode the window value, not all required parts detected in '-1.1 days'"),
    ('-1 .. 1',"Could not decode the window value, not all required parts detected in '-1 .. 1'"),
    (' .. 1 Weeks',"Could not decode the window value, not all required parts detected in ' .. 1 Weeks'")
  ]
  for index, test in enumerate(test_data):
    item = WindowType(test[0])
    assert item.errors == [test[1]]
