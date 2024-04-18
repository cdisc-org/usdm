import pytest
import pandas as pd
from usdm_excel.study_design_population_sheet.study_design_population_sheet import StudyDesignPopulationSheet
from usdm_model.characteristic import Characteristic

xfail = pytest.mark.xfail
def test_create(mocker, globals):
  mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
  mock_cross_ref.side_effect=[
    Characteristic(id="CH_1", name="CHAR_1", text='Something', instanceType='Characteristic'), 
    Characteristic(id="CH_2", name="CHAR_2", text='Something', instanceType='Characteristic'), 
    Characteristic(id="CH_3", name="CHAR_3", text='Something', instanceType='Characteristic')
  ]
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['R_1', 'R_2', 'X_3', 'R_4', 'Code_5', 'PopulationId_1', 'X_7', 'X_8', 'X_9', 'X_10', 'X_11', 'CohortId_1', 'X_13', 'X_14', 'X_15', 'X_16', 'X_17', 'CohortId_2', 'X_18', 'X_19', 'X_20']
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['MAIN',   'POP01', 'Main pop', 'Main Pop', 'BOTH',   '10..20', '100..110', '100..110 years', 'Y', ""], 
    ['COHORT', 'POP02', 'Cohort 1', 'Cohort 1', 'MALE',   '5..10',  '50..50',   '50..50 years',   'Y', "CHAR_1, CHAR_2"], 
    ['COHORT', 'POP03', 'Cohort 2', 'Cohort 2', 'FEMALE', '5..10',  '50..60',   '50..60 years',   'Y', "CHAR_3"], 
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['level', 'name', 'description', 'label', 'plannedSexOfParticipants', "plannedCompletionNumber", "plannedEnrollmentNumber", "plannedAge", 'includesHealthySubjects', 'characteristics'])
  item = StudyDesignPopulationSheet("", globals)
  assert item.population.id == 'PopulationId_1'
  assert item.population.name == 'POP01'
  assert item.population.description == 'Main pop'
  assert item.population.label == 'Main Pop'
  assert item.population.plannedEnrollmentNumber.id == 'R_2'
  assert item.population.plannedCompletionNumber.id == 'R_1'
  assert item.population.plannedSex[0].id == 'Code_5'
  assert item.population.plannedSex[0].decode == 'Both'
  assert item.population.plannedAge.id == 'R_4'
  assert item.population.cohorts[0].id == 'CohortId_1'
  assert item.population.cohorts[0].name == 'POP02'
  assert item.population.cohorts[0].characteristics[0].id == 'CH_1'
  assert item.population.cohorts[0].characteristics[1].id == 'CH_2'
  assert item.population.cohorts[1].id == 'CohortId_2'
  assert item.population.cohorts[1].name == 'POP03'
  assert item.population.cohorts[1].characteristics[0].id == 'CH_3'
  
def test_create_empty(mocker, globals):
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['category', 'identifier', 'name', 'description', 'label', 'text', 'dictionary'])
  items = StudyDesignPopulationSheet("", globals)
  assert items.population == None

def test_read_cell_by_name_error(mocker, globals):
  globals.cross_references.clear()
  call_parameters = []
  
  def my_add(sheet, row, column, message, level=10):
    call_parameters.append((sheet, row, column, message, level))
    return None

  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add", side_effect=my_add)
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    ['MAIN',   'POP01', 'Main pop', 'Main Pop', '10..20', '100..110', '100..110 years', 'Y', ""]
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=['level', 'name', 'description', 'label', "plannedCompletionNumber", "plannedEnrollmentNumber", "plannedAge", 'includesHealthySubjects', 'characteristics'])
  items = StudyDesignPopulationSheet("", globals)
  mock_error.assert_called()
  assert call_parameters == [
    ('studyDesignPopulations', None, None, "Exception. Error [Failed to detect column(s) 'plannedSexOfParticipants' in sheet] while reading sheet 'studyDesignPopulations'. See log for additional details.", 40)
  ]
  
