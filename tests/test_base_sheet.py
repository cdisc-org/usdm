import pytest
import pandas as pd

from src.usdm_excel.base_sheet import BaseSheet

def test_read_cell(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', '']}
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame.from_dict(data)
  base = BaseSheet("", "sheet")
  test_data = [
    (0,0,'3'),
    (3,0,'0'),
    (0,1,'a'),
    (3,1,'')
  ]
  for test in test_data:
    assert(base.read_cell(test[0],test[1])) == test[2]

def test_read_cell_error(mocker):
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', '']}
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame.from_dict(data)
  base = BaseSheet("", "sheet")
  assert(base.read_cell(6,8)) == ''
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "sheet"
  assert mock_error.call_args[0][1] == 7
  assert mock_error.call_args[0][2] == 9
  assert mock_error.call_args[0][3] == "Error (index 8 is out of bounds for axis 0 with size 2) reading cell"