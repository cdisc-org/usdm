import pytest
import pandas as pd
from usdm_excel.study_design_conditions_sheet.study_design_conditions_sheet import (
    StudyDesignConditionSheet,
)
from usdm_model.api_base_model import ApiBaseModelWithId


xfail = pytest.mark.xfail


def test_create(mocker, globals):
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [
        ApiBaseModelWithId(id="X1"),
        ApiBaseModelWithId(id="X2"),
        ApiBaseModelWithId(id="X3"),
        ApiBaseModelWithId(id="X4"),
        ApiBaseModelWithId(id="X5"),
        ApiBaseModelWithId(id="X6"),
        ApiBaseModelWithId(id="X7"),
        ApiBaseModelWithId(id="X8"),
        ApiBaseModelWithId(id="X9"),
        ApiBaseModelWithId(id="X10"),
    ]
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Cond_1", "Cond_2", "Cond_3", "Cond_4", "Cond_5"]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "Id 1",
            "Description One",
            "Label One",
            "Condition 1",
            "Context 1",
            "Applies 1",
        ],
        [
            "Id 2",
            "Description Two",
            "Label Two",
            "Condition 2",
            "Context 2",
            "Applies 2",
        ],
        [
            "Id 3",
            "Description Three",
            "Label Three",
            "Condition 3",
            "Context 3",
            "Applies 3",
        ],
        [
            "id 4",
            "Description Four",
            "Label Four",
            "Condition 4",
            "Context 4, context 5",
            "Applies 4",
        ],
        ["Id 5", "Description Five", "Label Five", "Condition 5", "", "Applies 5"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["name", "description", "label", "text", "context", "appliesTo"]
    )
    items = StudyDesignConditionSheet("", globals)
    assert len(items.items) == 5
    assert items.items[0].id == "Cond_1"
    assert items.items[0].name == "Id 1"
    assert items.items[0].description == "Description One"
    assert items.items[0].label == "Label One"
    assert items.items[0].contextIds == ["X1"]
    assert items.items[0].appliesToIds == ["X2"]
    assert items.items[3].contextIds == ["X7", "X8"]
    assert items.items[4].contextIds == []
    assert items.items[4].appliesToIds == ["X10"]


def test_create_with_commas(mocker, globals):
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [
        ApiBaseModelWithId(id="X1"),
        ApiBaseModelWithId(id="X2"),
        ApiBaseModelWithId(id="X3"),
        ApiBaseModelWithId(id="X4"),
        ApiBaseModelWithId(id="X5"),
        ApiBaseModelWithId(id="X6"),
        ApiBaseModelWithId(id="X7"),
        ApiBaseModelWithId(id="X8"),
        ApiBaseModelWithId(id="X9"),
        ApiBaseModelWithId(id="X10"),
    ]
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Cond_1", "Cond_2", "Cond_3", "Cond_4", "Cond_5"]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "Id 1",
            "Description One",
            "Label One",
            "Condition 1",
            "Context 1",
            "Applies 1",
        ],
        [
            "Id 2",
            "Description Two",
            "Label Two",
            "Condition 2",
            "Context 2",
            "Applies 2",
        ],
        [
            "Id 3",
            "Description Three",
            "Label Three",
            "Condition 3",
            "Context 3",
            "Applies 3",
        ],
        [
            "id 4",
            "Description Four",
            "Label Four",
            "Condition 4",
            '"Context, 4", context 5',
            '"Applies, 4"',
        ],
        ["Id 5", "Description Five", "Label Five", "Condition 5", "", "Applies 5"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["name", "description", "label", "text", "context", "appliesTo"]
    )
    items = StudyDesignConditionSheet("", globals)
    assert len(items.items) == 5
    assert items.items[0].id == "Cond_1"
    assert items.items[0].name == "Id 1"
    assert items.items[0].description == "Description One"
    assert items.items[0].label == "Label One"
    assert items.items[0].contextIds == ["X1"]
    assert items.items[0].appliesToIds == ["X2"]
    assert items.items[3].contextIds == ["X7", "X8"]
    assert items.items[3].appliesToIds == ["X9"]
    assert items.items[4].contextIds == []
    assert items.items[4].appliesToIds == ["X10"]


def test_create_empty(mocker, globals):
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["name", "description", "label", "text", "context", "appliesTo"]
    )
    items = StudyDesignConditionSheet("", globals)
    assert len(items.items) == 0


def test_missing_reference(mocker, globals):
    call_parameters = []

    def my_add(sheet, row, column, message, level=10):
        call_parameters.append((sheet, row, column, message, level))
        return None

    globals.cross_references.clear()
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [
        ApiBaseModelWithId(id="X1"),
        ApiBaseModelWithId(id="X2"),
    ]
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_error = mocker.patch(
        "usdm_excel.errors_and_logging.errors.Errors.add", side_effect=my_add
    )
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["Id 1", "Description One", "Condtition 1", "Label One", "Context 1", ""]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["name", "description", "label", "text", "context", "appliesTo"]
    )
    items = StudyDesignConditionSheet("", globals)
    mock_error.assert_called()
    assert call_parameters == [
        (
            "studyDesignConditions",
            1,
            6,
            "No condition references found for '', at least one required",
            40,
        )
    ]


def test_read_cell_by_name_error(mocker, globals):
    call_parameters = []

    def my_add(sheet, row, column, message, level=10):
        call_parameters.append((sheet, row, column, message, level))
        return None

    globals.cross_references.clear()
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [
        ApiBaseModelWithId(id="X1"),
        ApiBaseModelWithId(id="X2"),
    ]
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_error = mocker.patch(
        "usdm_excel.errors_and_logging.errors.Errors.add", side_effect=my_add
    )
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["Id 1", "Description One", "Label One", "Context 1", "Applies 1"]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["name", "description", "label", "context", "appliesTo"]
    )
    items = StudyDesignConditionSheet("", globals)
    mock_error.assert_called()
    assert call_parameters == [
        (
            "studyDesignConditions",
            1,
            -1,
            "Error attempting to read cell 'text'. Exception: Failed to detect column(s) 'text' in sheet",
            40,
        )
    ]
