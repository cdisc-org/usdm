import pytest
import pandas as pd

xfail = pytest.mark.xfail

from usdm_excel.study_design_indication_sheet.study_design_indication_sheet import StudyDesignIndicationSheet
from tests.test_utility import clear
from usdm_model.code import Code

def test_create(mocker):
  clear()
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['Code_1', 'IndicationId_1', 'Code_2', 'IndicationId_2', 'Code_3', 'Code_4', 'IndicationId_3']
  expected_1 = Code(id='Code_1', code='X', codeSystem='SPONSOR', codeSystemVersion='None set', decode="Y")
  expected_2 = Code(id='Code_2', code='AAA', codeSystem='SPONSOR', codeSystemVersion='None set', decode="BBB")
  expected_3 = Code(id='Code_3', code='WWW', codeSystem='SPONSOR', codeSystemVersion='None set', decode="1234")
  expected_4 = Code(id='Code_4', code='EEE', codeSystem='SPONSOR', codeSystemVersion='None set', decode="3456")
  mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
  mock_code.side_effect=[expected_1, expected_2, expected_3, expected_4]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['Indication 1', 'Indication One', 'Label One', 'Sponsor:X=Y'], 
          ['Indication 2', 'Indication Two', '', 'SPONSOR: AAA=BBB'], 
          ['Indication 3', 'Indication Three', '', 'SPONSOR: WWW=1234, SPONSOR: EEE=3456']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['name', 'description', 'label', 'codes'])
  Indications = StudyDesignIndicationSheet("")
  assert len(Indications.items) == 3
  assert Indications.items[0].id == 'IndicationId_1'
  assert Indications.items[0].name == 'Indication 1'
  assert Indications.items[1].id == 'IndicationId_2'
  assert Indications.items[1].description == 'Indication Two'
  assert Indications.items[1].codes == [expected_2]
  assert Indications.items[2].id == 'IndicationId_3'
  assert Indications.items[2].codes == [expected_3, expected_4]
  
def test_create_empty(mocker):
  clear()
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['studyIndicationName', 'studyIndicationDescription', 'studyIndicationType'])
  Indications = StudyDesignIndicationSheet("")
  assert len(Indications.items) == 0

def test_read_cell_by_name_error(mocker):
  clear()
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['Indication 1', 'Indication One']]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['name', 'description'])
  Indications = StudyDesignIndicationSheet("")
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyDesignIndications"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "Exception ['codes'] raised reading sheet."
  
