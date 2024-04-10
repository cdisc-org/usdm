import pandas as pd

from usdm_excel.configuration_sheet import ConfigurationSheet
from usdm_excel.option_manager import Options, EmptyNoneOption


def test_defaults(mocker, globals):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = {'col_1': ['Option X', 'Option 2', 'Option 3'], 'col_2': ['maybe', 'True', '']}
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data)
  configuration = ConfigurationSheet("", globals)
  assert globals.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.NONE.value

def test_sdr_deprecated(mocker, globals):
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = {'col_1': ['sdr DESCRIPTION'], 'col_2': ['']}
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data)
  configuration = ConfigurationSheet("", globals)
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "configuration"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "The SDR DESCRIPTION option is now deprecated and will be ignored."

def test_sdr_root_deprecated(mocker, globals):
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = {'col_1': ['SDR root'], 'col_2': ['']}
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data)
  configuration = ConfigurationSheet("", globals)
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "configuration"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "The SDR ROOT option is now deprecated and will be ignored."

def test_set_prev_next_deprecated(mocker, globals):
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = {'col_1': ['SDR prev next'], 'col_2': ['']}
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data)
  configuration = ConfigurationSheet("", globals)
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "configuration"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "The SDR PREV NEXT option is now deprecated and will be ignored."
