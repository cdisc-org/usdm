import pandas as pd
from usdm_excel.study_design_timing_sheet.study_design_timing_sheet import (
    StudyDesignTimingSheet,
)
from usdm_excel.study_design_timing_sheet.window_type import WindowType


def test_create(mocker, globals):
    globals.errors_and_logging.errors().clear()
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "Range1",
        "AC1",
        "Code1",
        "Code2",
        "X_1",
        "X_2",
        "TimingId_1",
        "Code3",
        "Code4",
        "TimingId_2",
        "Code5",
        "Code6",
        "TimingId_3",
        "X_5",
        "X_6",
        "X_5",
        "X_6",
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "Timing 1",
            "Timing One",
            "T1",
            "After",
            "X1",
            "X2",
            "3 days",
            "S2S",
            "-1..1 day",
        ],
        ["Timing 2", "Timing Two", "T2", "Before", "X2", "X3", "10 days", "E2S", ""],
        ["Timing 3", "Timing Three", "T3", "Fixed", "X4", "X5", "3 days", "e2e", ""],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "name",
            "description",
            "label",
            "type",
            "from",
            "to",
            "timingValue",
            "toFrom",
            "window",
        ],
    )

    items = StudyDesignTimingSheet("", globals)
    assert len(globals.errors_and_logging.errors().items) == 0
    assert len(items.items) == 3
    assert items.items[0].id == "TimingId_1"
    assert items.items[0].name == "Timing 1"
    assert items.items[0].description == "Timing One"
    assert items.items[0].type.decode == "After"
    assert items.items[1].id == "TimingId_2"
    assert items.items[1].description == "Timing Two"
    assert items.items[1].type.decode == "Before"
    assert items.items[2].id == "TimingId_3"
    assert items.items[2].type.decode == "Fixed Reference"


def test_window_type(mocker, globals):
    test_data = [
        ("1..1 Days", "P1D", "P1D", "1..1 Days"),
        (" -1..1 days", "P1D", "P1D", "-1..1 days"),
        ("-1 .. 1 weeks ", "P1W", "P1W", "-1 .. 1 weeks"),
        (None, None, None, ""),
    ]
    for index, test in enumerate(test_data):
        globals.errors_and_logging.errors().clear()
        item = WindowType(test[0], globals)
        assert (item.lower) == test[1]
        assert (item.upper) == test[2]
        assert (item.label) == test[3]
        assert (item.errors) == []


def test_window_type_error(mocker, globals):
    test_data = [
        (
            "1.. Days",
            "Could not decode the range value, possible typographical errors '1.. Days'",
        ),
        (
            "-1.1 days",
            "Could not decode the range value, possible typographical errors '-1.1 days'",
        ),
        (
            "-1 .. 1",
            "Could not decode the range value, possible typographical errors '-1 .. 1'",
        ),
        (" .. 1 Weeks", "Could not decode the range value '.. 1 Weeks'"),
    ]
    for index, test in enumerate(test_data):
        globals.errors_and_logging.errors().clear()
        item = WindowType(test[0], globals)
        assert item.errors == [test[1]]
