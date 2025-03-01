from tests.mocks.mock_general import *
from tests.mocks.mock_sheet import *
from tests.mocks.mock_ids import *
from tests.mocks.mock_logging import *
from usdm_model.study_amendment_impact import StudyAmendmentImpact
from usdm_excel.study_amendment_sheet.study_amendment_impact_sheet import (
    StudyAmendmentImpactSheet,
)
from usdm_model.code import Code


def test_create(mocker, globals):
    sheet_data = {
        "amendment": ["A1", "A2", "A3"],
        "text": ["Text One", "Text Two", "Text Three"],
        "substantial": [True, False, True],
        "type": ["xxx", "yyy", "zzz"],
    }
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
    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [expected_1, expected_2, expected_3]
    object_data = [
        {
            "cls": StudyAmendmentImpact,
            "data": {
                "text": sheet_data["text"][0],
                "isSubstantial": sheet_data["substantial"][0],
                "type": expected_1,
            },
        },
        {
            "cls": StudyAmendmentImpact,
            "data": {
                "text": sheet_data["text"][1],
                "isSubstantial": sheet_data["substantial"][1],
                "type": expected_2,
            },
        },
        {
            "cls": StudyAmendmentImpact,
            "data": {
                "text": sheet_data["text"][2],
                "isSubstantial": sheet_data["substantial"][2],
                "type": expected_3,
            },
        },
    ]
    mock_create_object(mocker, object_data)
    mock_sheet_present(mocker)
    mock_sheet(mocker, globals, sheet_data)
    item = StudyAmendmentImpactSheet("", globals)
    assert len(item.items) == 3
    assert item.items[0].model_dump() == {
        "id": "StudyAmendmentImpact_1",
        "instanceType": "StudyAmendmentImpact",
        "isSubstantial": True,
        "notes": [],
        "text": "Text One",
        "type": {
            "code": "X",
            "codeSystem": "SPONSOR",
            "codeSystemVersion": "",
            "decode": "Y",
            "id": "Code_1",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "extensionAttributes": [],
    }
    assert item.items[1].model_dump() == {
        "id": "StudyAmendmentImpact_2",
        "instanceType": "StudyAmendmentImpact",
        "isSubstantial": False,
        "notes": [],
        "text": "Text Two",
        "type": {
            "code": "AAA",
            "codeSystem": "SPONSOR",
            "codeSystemVersion": "",
            "decode": "BBB",
            "id": "Code_2",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "extensionAttributes": [],
    }
    assert item.items[2].model_dump() == {
        "id": "StudyAmendmentImpact_3",
        "instanceType": "StudyAmendmentImpact",
        "isSubstantial": True,
        "notes": [],
        "text": "Text Three",
        "type": {
            "code": "WWW",
            "codeSystem": "SPONSOR",
            "codeSystemVersion": "",
            "decode": "1234",
            "id": "Code_3",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "extensionAttributes": [],
    }


def test_create_empty(mocker, globals):
    sheet_data = {}
    mock_sheet_present(mocker)
    mock_sheet(mocker, globals, sheet_data)
    item = StudyAmendmentImpactSheet("", globals)
    assert len(item.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    sheet_data = {
        "amendment": ["A1"],
        "substantial": [True],
        "type": ["Y"],
    }
    expected_1 = Code(
        id="Code_1", code="X", codeSystem="SPONSOR", codeSystemVersion="", decode="Y"
    )
    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [expected_1]
    mea = mock_error_add(mocker, [None, None, None, None, None, None])
    mock_sheet_present(mocker)
    mock_sheet(mocker, globals, sheet_data)
    item = StudyAmendmentImpactSheet("", globals)
    assert mock_called(mea, 2)
    mock_parameters_correct(
        mea,
        [
            mocker.call(
                "amendmentImpact",
                1,
                -1,
                "Error attempting to read cell 'text'. Exception: Failed to detect column(s) 'text' in sheet",
                40,
            ),
            mocker.call(
                "amendmentImpact", 1, 1, "Failed to find amendment with name 'A1'", 40
            ),
        ],
    )
