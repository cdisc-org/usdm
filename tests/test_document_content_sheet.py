import pytest
import pandas as pd
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_definition_document.document_content_sheet import (
    DocumentContentSheet,
)
from usdm_excel.option_manager import Options, EmptyNoneOption
from tests.test_factory import Factory

xfail = pytest.mark.xfail


def test_create(mocker, globals):
    globals.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.EMPTY)

    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "Content_1",
        "Content_2",
        "Content_3",
        "Content_4",
        "Content_5",
        "Content_6",
        "Content_7",
        "Content_8",
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        ["ITEM1", "Text 1"],
        ["ITEM2", "Text 1.1"],
        ["ITEM3", "Text 1.2"],
        ["ITEM4", "Text 1.2.1"],
        ["ITEM5", "Text 2"],
        ["ITEM6", "Text 2.1"],
        ["ITEM7", "Text 3"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["name", "text"])
    content = DocumentContentSheet("", globals)
    assert len(content.items) == 7
    assert content.items[0].id == "Content_1"
    assert content.items[0].name == "ITEM1"
    assert (
        content.items[0].text
        == '<div xmlns="http://www.w3.org/1999/xhtml">Text 1</div>'
    )
    assert content.items[1].name == "ITEM2"
    assert content.items[2].name == "ITEM3"
    assert content.items[3].name == "ITEM4"
    assert content.items[4].name == "ITEM5"
    assert content.items[5].name == "ITEM6"
    assert content.items[6].id == "Content_7"
    assert content.items[6].name == "ITEM7"


def test_create_standard_section(mocker, globals):
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "Content_1",
        "Content_2",
        "Content_3",
        "Content_4",
        "Content_5",
        "Content_6",
        "Content_7",
        "Content_8",
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        ["ITEM1", "Text 1"],
        ["ITEM1", "Text 1.1"],
        ["ITEM1", '<usdm:section name="m11-title">'],
        ["ITEM1", '<div><usdm:section name="m11-title"></div>'],
        ["ITEM1", "Text 2"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["name", "text"])
    content = DocumentContentSheet("", globals)
    assert len(content.items) == 5
    assert (
        content.items[0].text
        == '<div xmlns="http://www.w3.org/1999/xhtml">Text 1</div>'
    )
    assert (
        content.items[1].text
        == '<div xmlns="http://www.w3.org/1999/xhtml">Text 1.1</div>'
    )
    assert (
        content.items[2].text
        == '<div xmlns="http://www.w3.org/1999/xhtml"><usdm:section name="m11-title"></div>'
    )
    assert (
        content.items[3].text
        == '<div xmlns="http://www.w3.org/1999/xhtml"><usdm:section name="m11-title"></div>'
    )
    assert (
        content.items[4].text
        == '<div xmlns="http://www.w3.org/1999/xhtml">Text 2</div>'
    )


def test_create_empty(mocker, globals):
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["sectionNumber", "name", "sectionTitle", "text"]
    )
    content = DocumentContentSheet("", globals)
    assert len(content.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    globals.template_manager.add("sponsor", "studyDesignContent")
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
    data = [["Section 1"]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["name"])
    content = DocumentContentSheet("", globals)
    assert mock_error.call_count == 1
    mock_error.assert_has_calls(
        [
            mocker.call(
                "documentContent",
                1,
                -1,
                "Error attempting to read cell 'text'. Exception: Failed to detect column(s) 'text' in sheet",
                40,
            )
        ]
    )
