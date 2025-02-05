import pytest
import pandas as pd
from usdm_excel.study_definition_document.document_template_sheet import (
    DocumentTemplateSheet,
)
from usdm_excel.option_manager import Options, EmptyNoneOption
from usdm_model.api_base_model import ApiBaseModelWithIdAndName

xfail = pytest.mark.xfail


def test_create(mocker, globals):
    globals.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.EMPTY)
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [
        ApiBaseModelWithIdAndName(id="X1", name="ITEM1"),
        ApiBaseModelWithIdAndName(id="X2", name="ITEM2"),
        ApiBaseModelWithIdAndName(id="X3", name="ITEM3"),
        ApiBaseModelWithIdAndName(id="X4", name="ITEM4"),
        ApiBaseModelWithIdAndName(id="X5", name="ITEM5"),
        ApiBaseModelWithIdAndName(id="X6", name="ITEM6"),
        ApiBaseModelWithIdAndName(id="X7", name="ITEM7"),
        ApiBaseModelWithIdAndName(id="X8", name="ITEM8"),
        ApiBaseModelWithIdAndName(id="X9", name="ITEM9"),
        ApiBaseModelWithIdAndName(id="X10", name="ITEM10"),
    ]
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
        ["CONTENT1", "1", True, "Section 1", True, "ITEM1"],
        ["CONTENT2", "1.1", True, "Section 1.1", True, "ITEM2"],
        ["CONTENT3", "1.2", True, "Section 1.2", True, "ITEM3"],
        ["CONTENT4", "1.2.1", True, "Section 1.2.1", True, "ITEM4"],
        ["CONTENT5", "2", True, "Section 2", True, "ITEM5"],
        ["CONTENT6", "2.1", True, "Section 2.1", True, "ITEM6"],
        ["CONTENT7", "3", True, "Section 3", True, "ITEM7"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "name",
            "sectionNumber",
            "displaySectionNumber",
            "sectionTitle",
            "displaySectionTitle",
            "content",
        ],
    )
    content = DocumentTemplateSheet("", "Template", "", globals)
    assert content.name == "Template"
    assert len(content.items) == 7
    assert content.items[0].name == "CONTENT1"
    assert content.items[0].previousId == ""
    assert content.items[0].nextId == "Content_2"
    assert content.items[0].childIds == ["Content_2", "Content_3"]
    assert content.items[1].id == "Content_2"
    assert content.items[1].name == "CONTENT2"
    assert content.items[1].sectionNumber == "1.1"
    assert content.items[1].sectionTitle == "Section 1.1"
    assert content.items[1].previousId == "Content_1"
    assert content.items[1].nextId == "Content_3"
    assert content.items[1].childIds == []
    assert content.items[2].id == "Content_3"
    assert content.items[2].name == "CONTENT3"
    assert content.items[2].previousId == "Content_2"
    assert content.items[2].nextId == "Content_4"
    assert content.items[2].childIds == ["Content_4"]
    assert content.items[3].id == "Content_4"
    assert content.items[3].name == "CONTENT4"
    assert content.items[3].previousId == "Content_3"
    assert content.items[3].nextId == "Content_5"
    assert content.items[3].childIds == []
    assert content.items[4].id == "Content_5"
    assert content.items[4].name == "CONTENT5"
    assert content.items[4].childIds == ["Content_6"]
    assert content.items[5].id == "Content_6"
    assert content.items[5].name == "CONTENT6"
    assert content.items[5].sectionNumber == "2.1"
    assert content.items[5].sectionTitle == "Section 2.1"
    assert content.items[5].childIds == []
    assert content.items[6].name == "CONTENT7"
    assert content.items[6].id == "Content_7"
    assert content.items[6].sectionNumber == "3"
    assert content.items[6].childIds == []


# def test_create_training_dot(mocker, globals):
#   mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
#   mock_present.side_effect=[True]
#   mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
#   mock_id.side_effect=['Content_1', 'Content_2', 'Content_3', 'Content_4', 'Content_5', 'Content_6', 'Content_7', 'Content_8']
#   mocked_open = mocker.mock_open(read_data="File")
#   mocker.patch("builtins.open", mocked_open)
#   data = [
#     ['1',     '',         'Section 1',     'Text 1'],
#     ['1.1',   'SET NAME', 'Section 1.1',   'Text 1.1'],
#     ['1.2',   '',         'Section 1.2',   'Text 1.2'],
#     ['1.2.1', '',         'Section 1.2.1', 'Text 1.2.1.'],
#     ['2',     '',         'Section 2',     'Text 2'],
#     ['2.1',   '',         'Section 2.1',   'Text 2.1.'],
#     ['3',     '',         'Section 3',     'Text 3'],
#   ]
#   mock_read = mocker.patch("pandas.read_excel")
#   mock_read.return_value = pd.DataFrame(data, columns=['name', 'sectionNumber', 'displaySectionNumber', 'sectionTitle', 'displaySectionTitle', 'content'])
#   content = DocumentTemplateSheet("", "", globals)
#   assert len(content.items) == 8
#   assert content.items[0].name == 'ROOT'
#   assert content.items[1].id == 'Content_2'
#   assert content.items[1].name == 'SECTION 1'
#   assert content.items[1].sectionNumber == '1'
#   assert content.items[1].sectionTitle == 'Section 1'
#   assert content.items[1].text == '<div xmlns="http://www.w3.org/1999/xhtml">Text 1</div>'
#   assert content.items[1].childIds == ['Content_3', 'Content_4']
#   assert content.items[2].name == 'SET NAME'
#   assert content.items[3].name == 'SECTION 1.2'
#   assert content.items[4].name == 'SECTION 1.2.1'
#   assert content.items[5].name == 'SECTION 2'
#   assert content.items[6].name == 'SECTION 2.1'
#   assert content.items[7].id == 'Content_8'
#   assert content.items[7].name == 'SECTION 3'


def test_create_4_levels(mocker, globals):
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [
        ApiBaseModelWithIdAndName(id="X1", name="ITEM1"),
        ApiBaseModelWithIdAndName(id="X2", name="ITEM2"),
        ApiBaseModelWithIdAndName(id="X3", name="ITEM3"),
        ApiBaseModelWithIdAndName(id="X4", name="ITEM4"),
        ApiBaseModelWithIdAndName(id="X5", name="ITEM5"),
        ApiBaseModelWithIdAndName(id="X6", name="ITEM6"),
        ApiBaseModelWithIdAndName(id="X7", name="ITEM7"),
        ApiBaseModelWithIdAndName(id="X8", name="ITEM8"),
        ApiBaseModelWithIdAndName(id="X9", name="ITEM9"),
        ApiBaseModelWithIdAndName(id="X10", name="ITEM10"),
    ]
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
        ["CONTENT1", "1", True, "Section 1", True, "ITEM1"],
        ["CONTENT2", "1.1", True, "Section 1.1", True, "ITEM2"],
        ["CONTENT3", "1.2", True, "Section 1.2", True, "ITEM3"],
        ["CONTENT4", "1.2.1", True, "Section 1.2.1", True, "ITEM4"],
        ["CONTENT5", "1.2.1.1", True, "Section 1.2.1.1", True, "ITEM5"],
        ["CONTENT6", "2", True, "Section 2", True, "ITEM6"],
        ["CONTENT7", "2.1", True, "Section 2.1", True, "ITEM7"],
        ["CONTENT8", "3", True, "Section 3", True, "ITEM8"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "name",
            "sectionNumber",
            "displaySectionNumber",
            "sectionTitle",
            "displaySectionTitle",
            "content",
        ],
    )
    content = DocumentTemplateSheet("", "Template", "", globals)
    assert len(content.items) == 8
    assert content.items[3].id == "Content_4"
    assert content.items[3].name == "CONTENT4"
    assert content.items[3].sectionNumber == "1.2.1"
    assert content.items[3].sectionTitle == "Section 1.2.1"
    assert content.items[3].childIds == ["Content_5"]
    assert content.items[4].id == "Content_5"
    assert content.items[4].name == "CONTENT5"
    assert content.items[4].sectionNumber == "1.2.1.1"
    assert content.items[4].displaySectionNumber == True
    assert content.items[4].sectionTitle == "Section 1.2.1.1"
    assert content.items[4].displaySectionTitle == True
    assert content.items[4].childIds == []


# def test_create_standard_section(mocker, globals):
#   mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
#   mock_present.side_effect=[True]
#   mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
#   mock_id.side_effect=['Content_1', 'Content_2', 'Content_3', 'Content_4', 'Content_5', 'Content_6', 'Content_7', 'Content_8']
#   mocked_open = mocker.mock_open(read_data="File")
#   mocker.patch("builtins.open", mocked_open)
#   data = [
#     ['1',       '',         'Section 1',       'Text 1'],
#     ['1.1',     'SET NAME', 'Section 1.1',     'Text 1.1'],
#     ['1.2',     '',         'Section 1.2',     '<usdm:section name="m11-title">'],
#     ['1.2.1',   '',         'Section 1.2.1',   '<div><usdm:section name="m11-title"></div>'],
#     ['2',       '',         'Section 2',       'Text 2'],
#   ]
#   mock_read = mocker.patch("pandas.read_excel")
#   mock_read.return_value = pd.DataFrame(data, columns=['sectionNumber', 'name', 'sectionTitle', 'text'])
#   content = DocumentTemplateSheet("", globals)
#   assert len(content.items) == 6
#   assert content.items[0].text == ''
#   assert content.items[1].text == '<div xmlns="http://www.w3.org/1999/xhtml">Text 1</div>'
#   assert content.items[2].text == '<div xmlns="http://www.w3.org/1999/xhtml">Text 1.1</div>'
#   assert content.items[3].text == '<div xmlns="http://www.w3.org/1999/xhtml"><usdm:section name="m11-title"></div>'
#   assert content.items[4].text == '<div xmlns="http://www.w3.org/1999/xhtml"><usdm:section name="m11-title"></div>'
#   assert content.items[5].text == '<div xmlns="http://www.w3.org/1999/xhtml">Text 2</div>'


def test_create_invalid_levels(mocker, globals):
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [
        ApiBaseModelWithIdAndName(id="X1", name="ITEM1"),
        ApiBaseModelWithIdAndName(id="X2", name="ITEM2"),
        ApiBaseModelWithIdAndName(id="X3", name="ITEM3"),
        ApiBaseModelWithIdAndName(id="X4", name="ITEM4"),
        ApiBaseModelWithIdAndName(id="X5", name="ITEM5"),
        ApiBaseModelWithIdAndName(id="X6", name="ITEM6"),
        ApiBaseModelWithIdAndName(id="X7", name="ITEM7"),
        ApiBaseModelWithIdAndName(id="X8", name="ITEM8"),
        ApiBaseModelWithIdAndName(id="X9", name="ITEM9"),
        ApiBaseModelWithIdAndName(id="X10", name="ITEM10"),
    ]
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
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
        ["CONTENT1", "1", True, "Section 1", True, "ITEM1"],
        ["CONTENT2", "1.1", True, "Section 1.1", True, "ITEM2"],
        ["CONTENT3", "1.2", True, "Section 1.2", True, "ITEM3"],
        ["CONTENT4", "1.2.1", True, "Section 1.2.1", True, "ITEM4"],
        ["CONTENT5", "1.2.1.1.4", True, "Section 1.2.1.1", True, "ITEM5"],
        ["CONTENT6", "2", True, "Section 2", True, "ITEM6"],
        ["CONTENT7", "2.1", True, "Section 2.1", True, "ITEM7"],
        ["CONTENT8", "3", True, "Section 3", True, "ITEM8"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "name",
            "sectionNumber",
            "displaySectionNumber",
            "sectionTitle",
            "displaySectionTitle",
            "content",
        ],
    )
    DocumentTemplateSheet("", "Template", "XXX", globals)
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "XXX"
    assert mock_error.call_args[0][1] == None
    assert mock_error.call_args[0][2] == None
    assert (
        mock_error.call_args[0][3]
        == "Exception. Error [] while reading sheet 'XXX'. See log for additional details."
    )


def test_create_empty(mocker, globals):
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "name",
            "sectionNumber",
            "displaySectionNumber",
            "sectionTitle",
            "displaySectionTitle",
            "content",
        ],
    )
    content = DocumentTemplateSheet("", "Template", "", globals)
    assert len(content.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    globals.cross_references.clear()
    globals.template_manager.add("sponsor", "studyDesignContent")
    call_parameters = []

    def my_add(sheet, row, column, message, level=10):
        call_parameters.append((sheet, row, column, message, level))
        return None

    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [ApiBaseModelWithIdAndName(id="X1", name="ITEM1")]
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_error = mocker.patch(
        "usdm_excel.errors_and_logging.errors.Errors.add", side_effect=my_add
    )
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["CONTENT1", "1", True, True, "ITEM1"]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "name",
            "sectionNumber",
            "displaySectionNumber",
            "displaySectionTitle",
            "content",
        ],
    )
    content = DocumentTemplateSheet("", "Template", "XXX", globals)
    mock_error.assert_called()
    assert call_parameters == [
        (
            "XXX",
            1,
            -1,
            "Error attempting to read cell 'sectionTitle'. Exception: Failed to detect column(s) 'sectionTitle' in sheet",
            40,
        )
    ]
