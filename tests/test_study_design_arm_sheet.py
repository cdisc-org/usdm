import pytest
import pandas as pd

xfail = pytest.mark.xfail

#from src.usdm_excel.base_sheet import BaseSheet
from src.usdm_excel.study_design_arm_sheet.study_design_arm_sheet import StudyDesignArmSheet
from src.usdm_model.code import Code

def test_create(mocker):
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['ArmId_1', 'ArmId_2', 'ArmId_3']
  expected_1 = Code(codeId='Code1', code='code', codeSystem='codesys', codeSystemVersion='3', decode="label1")
  expected_2 = Code(codeId='Code2', code='code', codeSystem='codesys', codeSystemVersion='3', decode="label2")
  expected_3 = Code(codeId='Code3', code='code', codeSystem='codesys', codeSystemVersion='3', decode="label3")
  expected_4 = Code(codeId='Code4', code='code', codeSystem='codesys', codeSystemVersion='3', decode="label4")
  expected_5 = Code(codeId='Code5', code='code', codeSystem='codesys', codeSystemVersion='3', decode="label5")
  expected_6 = Code(codeId='Code6', code='code', codeSystem='codesys', codeSystemVersion='3', decode="label6")
  mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
  mock_code.side_effect=[expected_1, expected_2, expected_3, expected_4, expected_5, expected_6]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['Arm 1', 'Arm One', 'C12345', 'Subject', 'C99999'], ['Arm 2', 'Arm Two', 'C12345', 'BYOD', 'C99999'], ['Arm 3', 'Arm Three', 'C12345', 'ePRO', 'C99999']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyArmName', 'studyArmDescription', 'studyArmType', 'studyArmDataOriginDescription', 'studyArmDataOriginType'])
  epochs = StudyDesignArmSheet("")
  assert len(epochs.items) == 3
  assert epochs.items[0].studyArmId == 'ArmId_1'
  assert epochs.items[0].studyArmName == 'Arm 1'
  assert epochs.items[0].studyArmDataOriginDescription == 'Subject'
  assert epochs.items[0].studyArmDataOriginType == expected_2
  assert epochs.items[1].studyArmId == 'ArmId_2'
  assert epochs.items[1].studyArmDescription == 'Arm Two'
  assert epochs.items[2].studyArmId == 'ArmId_3'
  assert epochs.items[2].studyArmType == expected_5
  assert epochs.items[2].studyArmDataOriginDescription == 'ePRO'
  
def test_create_empty(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyArmName', 'studyArmDescription', 'studyArmType'])
  epochs = StudyDesignArmSheet("")
  assert len(epochs.items) == 0

def test_read_cell_by_name_error(mocker):
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['Arm 1', 'Arm One']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyArmName', 'studyArmDescription'])
  epochs = StudyDesignArmSheet("")
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyDesignArms"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "Exception ['studyArmType'] raised reading sheet."
  
