import pytest
import pandas as pd

xfail = pytest.mark.xfail

from usdm_excel.study_design_encounter_sheet.study_design_encounter_sheet import StudyDesignEncounterSheet
from usdm_model.code import Code

def test_create(mocker):
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['RuleId_1', 'EncounterId_1', 'RuleId_2', 'EncounterId_2', 'EncounterId_3']
  codes = []
  for index in range(1,10):
    codes.append(Code(id=f'Code{index}', code='code', codeSystem='codesys', codeSystemVersion='3', decode=f"label{index}"))
  mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
  mock_code.side_effect = codes
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['E1', 'Encounter 1', 'Encounter One', 'visit', 'CLINIC', 'in Person', 'start rule', '' ], 
    ['E2', 'Encounter 2', 'Encounter Two', 'visit', 'CLINIC', 'in Person', '', 'end rule'], 
    ['E3', 'Encounter 3', 'Encounter Three', 'visit', 'HOME', 'TELEPHONE CALL', '', '']
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['xref', 'encounterName', 'encounterDescription', 'encounterType', 'encounterEnvironmentalSetting', 'encounterContactModes', 'transitionStartRule',	'transitionEndRule'])
  encounters = StudyDesignEncounterSheet("")
  assert len(encounters.items) == 3
  assert encounters.items[0].id == 'EncounterId_1'
  assert encounters.items[0].name == 'Encounter 1'
  assert encounters.items[1].id == 'EncounterId_2'
  assert encounters.items[1].description == 'Encounter Two'
  assert encounters.items[2].id == 'EncounterId_3'
  assert encounters.items[2].type == codes[6]
  
def test_create_with_label(mocker):
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")
  mock_id.side_effect=['RuleId_1', 'EncounterId_1', 'RuleId_2', 'EncounterId_2', 'EncounterId_3']
  codes = []
  for index in range(1,10):
    codes.append(Code(id=f'Code{index}', code='code', codeSystem='codesys', codeSystemVersion='3', decode=f"label{index}"))
  mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
  mock_code.side_effect = codes
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['E1', 'Encounter 1', 'Encounter One', '', 'visit', 'CLINIC', 'in Person', 'start rule', '' ], 
    ['E2', 'Encounter 2', 'Encounter Two', 'Label 2', 'visit', 'CLINIC', 'in Person', '', 'end rule'], 
    ['E3', 'Encounter 3', 'Encounter Three', 'Label 3', 'visit', 'HOME', 'TELEPHONE CALL', '', '']
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['xref', 'name', 'description', 'label', 'type', 'encounterEnvironmentalSetting', 'encounterContactModes', 'transitionStartRule',	'transitionEndRule'])
  encounters = StudyDesignEncounterSheet("")
  assert len(encounters.items) == 3
  assert encounters.items[0].id == 'EncounterId_1'
  assert encounters.items[0].name == 'Encounter 1'
  assert encounters.items[0].label == ''
  assert encounters.items[1].id == 'EncounterId_2'
  assert encounters.items[1].description == 'Encounter Two'
  assert encounters.items[2].id == 'EncounterId_3'
  assert encounters.items[2].type == codes[6]
  assert encounters.items[2].label == 'Label 3'

def test_create_empty(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['xref', 'encounterName', 'encounterDescription', 'encounterType', 'encounterEnvironmentalSetting', 'encounterContactModes', 'transitionStartRule',	'transitionEndRule'])
  encounters = StudyDesignEncounterSheet("")
  assert len(encounters.items) == 0

def test_read_cell_by_name_error(mocker):
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['E1', 'Encounter 1', 'Encounter One', 'CLINIC', 'in Person', 'start rule', '' ]]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['xref', 'encounterName', 'encounterDescription', 'encounterEnvironmentalSetting', 'encounterContactModes', 'transitionStartRule',	'transitionEndRule'])
  encounters = StudyDesignEncounterSheet("")
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyDesignEncounters"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "Exception [Failed to detect column(s) 'encounterType, type' in sheet] raised reading sheet."
  
