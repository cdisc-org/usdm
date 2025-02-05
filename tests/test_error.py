from usdm_excel.errors_and_logging.error import Error


def test_create():
    error = Error(sheet="My Sheet", row=1, column=99, message="XXXXX")
    assert error.sheet == "My Sheet"
    assert error.row == 1
    assert error.column == 99
    assert error.message == "XXXXX"


def test_to_log():
    error = Error(sheet="My Sheet", row=1, column=99, message="XXXXX")
    assert (error.to_log()) == "Error in sheet My Sheet at [1,99]: XXXXX"
    error = Error(sheet="My Sheet", row=None, column=None, message="XXXXX")
    assert (error.to_log()) == "Error in sheet My Sheet: XXXXX"
    error = Error(sheet=None, row=None, column=None, message="XXXXX")
    assert (error.to_log()) == "Error: XXXXX"


def test_to_dict():
    error = Error(sheet="My Sheet", row=1, column=99, message="XXXXX")
    assert (error.to_dict()) == {
        "sheet": "My Sheet",
        "row": 1,
        "column": 99,
        "message": "XXXXX",
        "level": "Error",
    }
