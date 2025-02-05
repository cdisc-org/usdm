import pytest
import pandas as pd
from usdm_excel.study_design_characteristics_sheet.study_design_characteristics_sheet import (
    StudyDesignCharacteristicSheet,
)

xfail = pytest.mark.xfail


def test_create(mocker, globals):
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "CharacteristicId_1",
        "CharacteristicId_2",
        "CharacteristicId_3",
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "CHAR01",
            "The study age characteristic",
            "Age characteristic",
            "Subjects should be between 18 and 45 years old",
            "dictionary",
        ],
        [
            "CHAR02",
            "The study abc characteristic",
            "ABC characteristic",
            "Subjects should have ABC",
            "dictionary",
        ],
        [
            "CHAR03",
            "Exclude those with all fingers",
            "Fingers characteristic",
            "Subjects should not have all fingers",
            "dictionary",
        ],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["name", "description", "label", "text", "dictionary"]
    )
    items = StudyDesignCharacteristicSheet("", globals)
    assert len(items.items) == 3
    assert items.items[0].id == "CharacteristicId_1"
    assert items.items[0].name == "CHAR01"
    assert items.items[0].description == "The study age characteristic"
    assert items.items[0].label == "Age characteristic"
    assert items.items[0].text == "Subjects should be between 18 and 45 years old"


def test_create_empty(mocker, globals):
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["name", "description", "label", "text", "dictionary"]
    )
    items = StudyDesignCharacteristicSheet("", globals)
    assert len(items.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    globals.cross_references.clear()
    call_parameters = []

    def my_add(sheet, row, column, message, level=10):
        call_parameters.append((sheet, row, column, message, level))
        return None

    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_error = mocker.patch(
        "usdm_excel.errors_and_logging.errors.Errors.add", side_effect=my_add
    )
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "The study age characteristic",
            "Age characteristic",
            "Subjects should be between 18 and 45 years old",
            "dictionary",
        ]
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["name", "description", "label", "dictionary"]
    )
    items = StudyDesignCharacteristicSheet("", globals)
    mock_error.assert_called()
    assert call_parameters == [
        (
            "studyDesignCharacteristics",
            1,
            -1,
            "Error attempting to read cell 'text'. Exception: Failed to detect column(s) 'text' in sheet",
            40,
        ),
        (
            "studyDesignCharacteristics",
            None,
            None,
            "Exception. Error [Failed to detect column(s) 'text' in sheet] while reading sheet 'studyDesignCharacteristics'. See log for additional details.",
            40,
        ),
    ]
