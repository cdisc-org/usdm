import pytest
import pandas as pd

from src.usdm_excel.base_sheet import BaseSheet

def test_read_cell(mocker):
    data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
    mock_xxx = mocker.patch("src.usdm_excel.base_sheet.pd")
    mock_xxx.read_excel.return_value = pd.DataFrame.from_dict(data)

    base = BaseSheet("", "sheet")
    assert(base.read_cell(0,0)) == "3"
