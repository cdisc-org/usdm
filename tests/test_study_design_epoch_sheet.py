import pytest
import pandas as pd

xfail = pytest.mark.xfail

#from src.usdm_excel.base_sheet import BaseSheet
from src.usdm_excel.study_design_epoch_sheet.study_design_epoch_sheet import StudyDesignEpochSheet
from src.usdm_model.code import Code

def test_create(mocker):
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['EpochId_1', 'EpochId_2', 'EpochId_3']
  expected_1 = Code(codeId='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="label1")
  expected_2 = Code(codeId='Code2', code='code', codeSystem='codesys', codeSystemVersion='3', decode="label2")
  expected_3 = Code(codeId='Code3', code='code', codeSystem='codesys', codeSystemVersion='3', decode="label3")
  mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
  mock_code.side_effect=[expected_1, expected_2, expected_3]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['Epoch 1', 'Epoch One', 'C12345'], ['Epoch 2', 'Epoch Two', 'C12345'], ['Epoch 3', 'Epoch Three', 'C12345']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyEpochName', 'studyEpochDescription', 'studyEpochType'])
  epochs = StudyDesignEpochSheet("")
  assert len(epochs.items) == 3
  assert epochs.items[0].studyEpochId == 'EpochId_1'
  assert epochs.items[0].studyEpochName == 'Epoch 1'
  assert epochs.items[1].studyEpochId == 'EpochId_2'
  assert epochs.items[1].studyEpochDescription == 'Epoch Two'
  assert epochs.items[2].studyEpochId == 'EpochId_3'
  assert epochs.items[2].studyEpochType == expected_3
  
def test_create_empty(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyEpochName', 'studyEpochDescription', 'studyEpochType'])
  epochs = StudyDesignEpochSheet("")
  assert len(epochs.items) == 0

def test_read_cell_by_name_error(mocker):
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['Epoch 1', 'Epoch One']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyEpochName', 'studyEpochDescription'])
  epochs = StudyDesignEpochSheet("")
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyDesignEpochs"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "Exception ['studyEpochType'] raised reading sheet."
  
