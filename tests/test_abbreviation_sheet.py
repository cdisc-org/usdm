import pytest
import pandas as pd
from usdm_excel.abbreviation_sheet.abbreviation_sheet import AbbreviationSheet
from usdm_model.comment_annotation import CommentAnnotation
from usdm_excel.globals import Globals
from tests.test_factory import Factory

xfail = pytest.mark.xfail


def test_create(mocker, globals):
    data = {
        "abbreviatedText": ["A1", "A2", "A3"],
        "expandedText": [
            "Annotation Text One",
            "Annotation Text Two",
            "Annotaiton Text Three",
        ],
    }
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Abbreviation_1", "Abbreviation_2", "Abbreviation_3"]
    _setup(mocker, globals, data)
    item = AbbreviationSheet("", globals)
    assert len(item.items) == 3
    assert item.items[0].id == "Abbreviation_1"
    assert item.items[0].abbreviatedText == "A1"
    assert item.items[1].id == "Abbreviation_2"
    assert item.items[1].abbreviatedText == "A2"
    assert item.items[1].expandedText == "Annotation Text Two"
    assert item.items[2].id == "Abbreviation_3"
    assert item.items[2].abbreviatedText == "A3"


def test_create_with_notes(factory, mocker, globals):
    data = {
        "abbreviatedText": ["A1"],
        "expandedText": ["Annotation Text One"],
        "notes": "N1, N2",
    }
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Note_1", "Note_2", "Note_3", "Abbreviation_1"]
    _setup(mocker, globals, data)
    _create_notes(factory, globals)
    item = AbbreviationSheet("", globals)
    assert len(item.items) == 1
    assert item.items[0].id == "Abbreviation_1"
    assert item.items[0].abbreviatedText == "A1"
    assert item.items[0].notes[0].text == "Note 1"
    assert item.items[0].notes[0].codes == []


def test_create_empty(mocker, globals):
    data = {}
    _setup(mocker, globals, data)
    item = AbbreviationSheet("", globals)
    assert len(item.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    data = {
        "abbreviatedText": ["A1"],
    }
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Code_1", "Abbreviation_1"]
    _setup(mocker, globals, data)
    item = AbbreviationSheet("", globals)
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "abbreviations"
    assert mock_error.call_args[0][1] == None
    assert mock_error.call_args[0][2] == None
    assert (
        mock_error.call_args[0][3]
        == "Exception. Failed to create Abbreviation object. See log for additional details."
    )


def _setup(mocker, globals, data):
    globals.cross_references.clear()
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)


def _create_notes(factory: Factory, globals: Globals):
    notes = {
        "N1": {"text": "Note 1", "codes": []},
        "N2": {"text": "Note 2", "codes": []},
        "N3": {"text": "Note 3", "codes": []},
    }
    for name, note in notes.items():
        item = factory.item(CommentAnnotation, note)
        globals.cross_references.add(name, item)
