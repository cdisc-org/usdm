import pytest
import pandas as pd
from usdm_excel.annotation_sheet.annotation_sheet import AnnotationSheet
from usdm_model.code import Code

xfail = pytest.mark.xfail


def test_create(mocker, globals):
    data = {
        "name": ["A1", "A2", "A3"],
        "text": ["Annotation Text One", "Annotation Text Two", "Annotaiton Text Three"],
        "codes": [
            "Sponsor:X=Y",
            "SPONSOR: AAA=BBB",
            "SPONSOR: WWW=1234, SPONSOR: EEE=3456",
        ],
    }
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "Code_1",
        "CommentAnnotation_1",
        "Code_2",
        "CommentAnnotation_2",
        "Code_3",
        "Code_4",
        "CommentAnnotation_3",
    ]
    _setup(mocker, globals, data)
    expected_1 = Code(
        id="Code_1", code="X", codeSystem="SPONSOR", codeSystemVersion="", decode="Y"
    )
    expected_2 = Code(
        id="Code_2",
        code="AAA",
        codeSystem="SPONSOR",
        codeSystemVersion="",
        decode="BBB",
    )
    expected_3 = Code(
        id="Code_3",
        code="WWW",
        codeSystem="SPONSOR",
        codeSystemVersion="",
        decode="1234",
    )
    expected_4 = Code(
        id="Code_4",
        code="EEE",
        codeSystem="SPONSOR",
        codeSystemVersion="",
        decode="3456",
    )
    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [expected_1, expected_2, expected_3, expected_4]
    item = AnnotationSheet("", globals)
    assert len(item.items) == 3
    assert item.items[0].id == "CommentAnnotation_1"
    assert item.items[1].id == "CommentAnnotation_2"
    assert item.items[1].text == "Annotation Text Two"
    assert item.items[1].codes == [expected_2]
    assert item.items[2].id == "CommentAnnotation_3"
    assert item.items[2].codes == [expected_3, expected_4]


def test_create_empty(mocker, globals):
    data = {}
    _setup(mocker, globals, data)
    item = AnnotationSheet("", globals)
    assert len(item.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    data = {"name": ["A1"], "codes": ["Sponsor:X=Y"]}
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Code_1", "CommentAnnotation_1"]
    _setup(mocker, globals, data)
    item = AnnotationSheet("", globals)
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "notes"
    assert mock_error.call_args[0][1] == 1
    assert mock_error.call_args[0][2] == -1
    assert (
        mock_error.call_args[0][3]
        == "Error attempting to read cell 'text'. Exception: Failed to detect column(s) 'text' in sheet"
    )


def _setup(mocker, globals, data):
    globals.cross_references.clear()
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
