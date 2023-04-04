import pytest
import pandas as pd

from src.usdm_excel.base_sheet import BaseSheet

def test_read_cell(mocker):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    base = BaseSheet("", "sheet")
    assert(base.read_cell(0,0)) == "3"
