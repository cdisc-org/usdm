import pytest
import json
import pandas as pd
from usdm_excel.study_design_intervention_sheet.study_design_intervention_sheet import StudyDesignInterventionSheet
from usdm_model.code import Code


xfail = pytest.mark.xfail

SAVE = True
COLUMNS = [ 'name', 'description', 'label', "codes", "role", "type", 
  "pharmacologicalClass", "productDesignation", "minimumResponseDuration", 'administrationName', 'administrationDescription', 
  'administrationLabel', "administrationRoute", "administrationDose", "administrationFrequency", 
  'administrationDurationDescription', 'administrationDurationWillVary', 'administrationDurationWillVaryReason', 'administrationDurationQuantity' ]

def read_json(filename):
  with open(filename, 'r') as f:
    data = json.load(f)
  return data

def dump_json(data):
  print(f"\n{json.dumps(data, indent=2)}")

def test_create(mocker, globals):
  expected = read_json(f"tests/integration_test_files/intervention/create.json")
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=[f"Id_{x}" for x in range(100)]

  mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
  mock_code.side_effect=[Code(id=f'Code_{x}', code='C12345', codeSystem='CDISC', codeSystemVersion='1', decode=f"INDEX{x}") for x in range(100)]
  
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    # name     description    label          codes                          role                         type      pharmacologicalClass  productDesignation      minimumResponseDuration,  administrationName [10] administrationDescription administrationLabel administrationRoute administrationDose administrationFrequency administrationDurationDescription administrationDurationWillVary administrationDurationWillVaryReason administrationDurationQuantity
    [ 'Int 1', 'Int Desc 1',  'Int Label 1', 'SPONSOR: A=B',                'Experimental Intervention', 'C12345', 'FDA: A=B',           'IMP',                  '1 Day',                  'Admin 1',              'Admin Desc 1',           'Admin Label 1',    'C34567',          '12 mg',            'C65432',               'Dur desc 1',                     'False',                       '',                                  '14 %'                         ], 
    [ '',      '',            '',            '',                            '',                          '',       '',                   '',                     '',                       'Admin 2',              'Admin Desc 2',           'Admin Label 1',    'C34567',          '1 mg',             'C65432',               'Dur desc 1',                     'False',                       '',                                  '10 m'                         ], 
    [ 'Int 2', 'Int Desc 2',  'Int Label 2', 'SPONSOR: C=D',                'Placebo',                   'C12345', 'FDA: A=B',           'NIMP (AxMP)',          '3 Weeks',                'Admin 3',              'Admin Desc 3',           'Admin Label 1',    'C34567',          '100 mg',           'C65432',               'Dur desc 1',                     'False',                       '',                                  '12 C'                         ], 
    [ 'Int 3', 'Int Desc 3',  'Int Label 3', 'SPONSOR: E=F, SPONSOR: G=H',  'Rescue Medicine',           'C12345', 'FDA: A=B',           'IMP',                  '4 Years',                'Admin 4',              'Admin Desc 4',           'Admin Label 1',    'C34567',          '500 mg',           'C65432',               'Dur desc 1',                     'False',                       '',                                  '12 F'                         ], 
    [ '',      '',            '',            '',                            '',                          '',       '',                   '',                     '',                       'Admin 5',              'Admin Desc 5',           'Admin Label 1',    'C34567',          '1 mg',             'C65432',               'Dur desc 1',                     'False',                       '',                                  '15 in'                        ], 
  ]

  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=COLUMNS)
  interventions = StudyDesignInterventionSheet("", globals)
  #dump_json({'items': [json.loads(x.to_json()) for x in interventions.items]})
  for index, item in enumerate(interventions.items):
    result = json.loads(item.to_json())
    assert result == expected["items"][index]
  
def test_create_empty(mocker, globals):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=COLUMNS)
  interventions = StudyDesignInterventionSheet("", globals)
  assert len(interventions.items) == 0

def test_read_cell_by_name_error(mocker, globals):
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']]
  mock_read = mocker.patch("pandas.read_excel")
  columns = COLUMNS
  columns = columns[0:-1]
  mock_read.return_value = pd.DataFrame(data, columns=columns)
  interventions = StudyDesignInterventionSheet("", globals)
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyDesignInterventions"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "Exception. Error [Failed to detect column(s) 'administrationDurationQuantity' in sheet] while reading sheet 'studyDesignInterventions'. See log for additional details."
  
