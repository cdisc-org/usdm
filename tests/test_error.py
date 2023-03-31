import pytest

from src.usdm_excel.errors.error import Error

def test_create():
    error = Error(sheet="My Sheet", row=1, column=99, message="XXXXX")
    assert error.sheet == "My Sheet"
    assert error.row == 1
    assert error.column == 99
    assert error.message == "XXXXX"
