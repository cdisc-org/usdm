import pytest
import pandas as pd
from usdm_excel.study_design_arm_sheet.study_design_arm_sheet import StudyDesignArmSheet
from usdm_model.code import Code


xfail = pytest.mark.xfail


def test_create(mocker, globals):
    globals.cross_references.clear()
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["ArmId_1", "ArmId_2", "ArmId_3"]
    expected_1 = Code(
        id="Code1",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label1",
    )
    expected_2 = Code(
        id="Code2",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label2",
    )
    expected_3 = Code(
        id="Code3",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label3",
    )
    expected_4 = Code(
        id="Code4",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label4",
    )
    expected_5 = Code(
        id="Code5",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label5",
    )
    expected_6 = Code(
        id="Code6",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label6",
    )
    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [
        expected_1,
        expected_2,
        expected_3,
        expected_4,
        expected_5,
        expected_6,
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        ["Arm 1", "Arm One", "C12345", "Subject", "C99999"],
        ["Arm 2", "Arm Two", "C12345", "BYOD", "C99999"],
        ["Arm 3", "Arm Three", "C12345", "ePRO", "C99999"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "studyArmName",
            "studyArmDescription",
            "studyArmType",
            "studyArmDataOriginDescription",
            "studyArmDataOriginType",
        ],
    )
    arms = StudyDesignArmSheet("", globals)
    assert len(arms.items) == 3
    assert arms.items[0].id == "ArmId_1"
    assert arms.items[0].name == "Arm 1"
    assert arms.items[0].label == ""
    assert arms.items[0].dataOriginDescription == "Subject"
    assert arms.items[0].dataOriginType == expected_2
    assert arms.items[1].id == "ArmId_2"
    assert arms.items[1].description == "Arm Two"
    assert arms.items[2].id == "ArmId_3"
    assert arms.items[2].type == expected_5
    assert arms.items[2].dataOriginDescription == "ePRO"


def test_create_with_name_and_label(mocker, globals):
    globals.cross_references.clear()
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["ArmId_1", "ArmId_2", "ArmId_3"]
    expected_1 = Code(
        id="Code1",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label1",
    )
    expected_2 = Code(
        id="Code2",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label2",
    )
    expected_3 = Code(
        id="Code3",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label3",
    )
    expected_4 = Code(
        id="Code4",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label4",
    )
    expected_5 = Code(
        id="Code5",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label5",
    )
    expected_6 = Code(
        id="Code6",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label6",
    )
    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [
        expected_1,
        expected_2,
        expected_3,
        expected_4,
        expected_5,
        expected_6,
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        ["Arm 1", "Arm One", "Arm 1", "C12345", "Subject", "C99999"],
        ["Arm 2", "Arm Two", "Arm 2", "C12345", "BYOD", "C99999"],
        ["Arm 3", "Arm Three", "Arm Tre", "C12345", "ePRO", "C99999"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "name",
            "description",
            "label",
            "type",
            "studyArmDataOriginDescription",
            "dataOriginType",
        ],
    )
    arms = StudyDesignArmSheet("", globals)
    assert len(arms.items) == 3
    assert arms.items[0].id == "ArmId_1"
    assert arms.items[0].name == "Arm 1"
    assert arms.items[0].description == "Arm One"
    assert arms.items[0].label == "Arm 1"
    assert arms.items[0].dataOriginDescription == "Subject"
    assert arms.items[0].dataOriginType == expected_2
    assert arms.items[1].id == "ArmId_2"
    assert arms.items[1].description == "Arm Two"
    assert arms.items[2].id == "ArmId_3"
    assert arms.items[2].type == expected_5
    assert arms.items[2].dataOriginDescription == "ePRO"


def test_create_empty(mocker, globals):
    globals.cross_references.clear()
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["studyArmName", "studyArmDescription", "studyArmType"]
    )
    arms = StudyDesignArmSheet("", globals)
    assert len(arms.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    globals.cross_references.clear()
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["Arm 1", "Arm One"]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["studyArmName", "studyArmDescription"]
    )
    arms = StudyDesignArmSheet("", globals)
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "studyDesignArms"
    assert mock_error.call_args[0][1] == None
    assert mock_error.call_args[0][2] == None
    assert (
        mock_error.call_args[0][3]
        == "Exception. Error [Failed to detect column(s) 'studyArmType, type' in sheet] while reading sheet 'studyDesignArms'. See log for additional details."
    )
