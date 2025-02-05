import pytest
import pandas as pd
from usdm_excel.study_design_epoch_sheet.study_design_epoch_sheet import (
    StudyDesignEpochSheet,
)
from usdm_model.code import Code


xfail = pytest.mark.xfail


def test_create(mocker, globals):
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["EpochId_1", "EpochId_2", "EpochId_3"]
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
    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [expected_1, expected_2, expected_3]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        ["Epoch 1", "Epoch One", "C12345"],
        ["Epoch 2", "Epoch Two", "C12345"],
        ["Epoch 3", "Epoch Three", "C12345"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["studyEpochName", "studyEpochDescription", "studyEpochType"]
    )
    epochs = StudyDesignEpochSheet("", globals)
    assert len(epochs.items) == 3
    assert epochs.items[0].id == "EpochId_1"
    assert epochs.items[0].name == "Epoch 1"
    assert epochs.items[1].id == "EpochId_2"
    assert epochs.items[1].description == "Epoch Two"
    assert epochs.items[2].id == "EpochId_3"
    assert epochs.items[2].type == expected_3


def test_create_with_label(mocker, globals):
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["EpochId_1", "EpochId_2", "EpochId_3"]
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
    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [expected_1, expected_2, expected_3]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        ["Epoch 1", "Epoch One", "1", "C12345"],
        ["Epoch 2", "Epoch Two", "2", "C12345"],
        ["Epoch 3", "Epoch Three", "", "C12345"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["name", "description", "label", "studyEpochType"]
    )
    epochs = StudyDesignEpochSheet("", globals)
    assert len(epochs.items) == 3
    assert epochs.items[0].id == "EpochId_1"
    assert epochs.items[0].name == "Epoch 1"
    assert epochs.items[0].label == "1"
    assert epochs.items[1].id == "EpochId_2"
    assert epochs.items[1].description == "Epoch Two"
    assert epochs.items[2].id == "EpochId_3"
    assert epochs.items[2].type == expected_3
    assert epochs.items[2].label == ""


def test_create_empty(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["studyEpochName", "studyEpochDescription", "studyEpochType"]
    )
    epochs = StudyDesignEpochSheet("", globals)
    assert len(epochs.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["Epoch 1", "Epoch One"]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["studyEpochName", "studyEpochDescription"]
    )
    epochs = StudyDesignEpochSheet("", globals)
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "studyDesignEpochs"
    assert mock_error.call_args[0][1] == None
    assert mock_error.call_args[0][2] == None
    assert (
        mock_error.call_args[0][3]
        == "Exception. Error [Failed to detect column(s) 'studyEpochType, type' in sheet] while reading sheet 'studyDesignEpochs'. See log for additional details."
    )
