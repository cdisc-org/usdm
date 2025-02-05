import pytest
import pandas as pd
from usdm_excel.study_design_dictionary_sheet.study_design_dictionary_sheet import (
    StudyDesignDictionarySheet,
)
from usdm_model.api_base_model import ApiBaseModelWithId


xfail = pytest.mark.xfail


def test_create(mocker, globals):
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [
        ApiBaseModelWithId(id="1"),
        ApiBaseModelWithId(id="2"),
        ApiBaseModelWithId(id="3"),
        ApiBaseModelWithId(id="4"),
        ApiBaseModelWithId(id="5"),
    ]
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "DictionaryId_1",
        "MapId_1",
        "MapId_2",
        "DictionaryId_2",
        "MapId_3",
        "DictionaryId_3",
        "MapId_4",
        "MapId_5",
        "MapId_6",
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "Dictionary 1",
            "Dictionary One",
            "Label One",
            "Key 1",
            ApiBaseModelWithId,
            "Id 1",
            "Attribute 1",
            "",
        ],
        ["", "", "", "Key 2", ApiBaseModelWithId, "Id 2", "Attribute 2", ""],
        [
            "Dictionary 2",
            "Dictionary Two",
            "Label Two",
            "Key 3",
            ApiBaseModelWithId,
            "Id 3",
            "Attribute 3",
            "",
        ],
        [
            "Dictionary 3",
            "Dictionary Three",
            "Label Three",
            "Key 4",
            ApiBaseModelWithId,
            "Id 4",
            "Attribute 4",
            "",
        ],
        ["", "", "", "Key 5", ApiBaseModelWithId, "Id 5", "Attribute 5", ""],
        ["", "", "", "Key 6", "", "", "", "Hello!"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "name",
            "description",
            "label",
            "key",
            "class",
            "xref",
            "attribute",
            "value",
        ],
    )
    dictionaries = StudyDesignDictionarySheet("", globals)
    assert len(dictionaries.items) == 3
    assert dictionaries.items[0].id == "DictionaryId_1"
    assert dictionaries.items[0].name == "Dictionary 1"
    assert dictionaries.items[0].description == "Dictionary One"
    assert dictionaries.items[0].label == "Label One"
    assert dictionaries.items[0].parameterMaps[1].tag == "Key 2"
    assert (
        dictionaries.items[0].parameterMaps[1].reference
        == '<usdm:ref klass="ApiBaseModelWithId" id="2" attribute="Attribute 2"></usdm:ref>'
    )
    assert [x.tag for x in dictionaries.items[1].parameterMaps] == ["Key 3"]
    assert [x.tag for x in dictionaries.items[2].parameterMaps] == [
        "Key 4",
        "Key 5",
        "Key 6",
    ]
    assert dictionaries.items[2].parameterMaps[2].reference == "Hello!"


def test_create_empty(mocker, globals):
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=["name", "description", "label", "key", "class", "xref", "attribute"],
    )
    dictionaries = StudyDesignDictionarySheet("", globals)
    assert len(dictionaries.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    call_parameters = []

    def my_add(sheet, row, column, message, level=10):
        call_parameters.append((sheet, row, column, message, level))
        return None

    globals.cross_references.clear()
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_error = mocker.patch(
        "usdm_excel.errors_and_logging.errors.Errors.add", side_effect=my_add
    )
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "Dictionary 1",
            "Dictionary One",
            "Label One",
            "Key 1",
            "Klass 1",
            "Attribute 1",
        ]
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["name", "description", "label", "key", "class", "attribute"]
    )
    dictionaries = StudyDesignDictionarySheet("", globals)
    mock_error.assert_called()
    assert call_parameters == [
        (
            "dictionaries",
            1,
            -1,
            "Error attempting to read cell 'xref'. Exception: Failed to detect column(s) 'xref' in sheet",
            40,
        ),
        (
            "dictionaries",
            1,
            6,
            "Failed to translate reference path 'Attribute 1', could not find start instance 'Klass 1', ''",
            40,
        ),
    ]
