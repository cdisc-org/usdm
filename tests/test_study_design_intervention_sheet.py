import pytest
import pandas as pd

xfail = pytest.mark.xfail

from usdm_excel.study_design_intervention_sheet.study_design_intervention_sheet import StudyDesignInterventionSheet
from usdm_model.code import Code

COLUMNS = [ 'name', 'description', 'label', "codes", "role", "type", 
  "pharmacologicalClass", "productDesignation", "minimumResponseDuration", 'administrationName', 'administrationDescription', 
  'administrationLabel', "administrationRoute", "administrationDose", "administrationFrequency", 
  'administrationDurationDescription', 'administrationDurationWillVary', 'administrationDurationWillVaryReason', 'administrationDurationQuantity' ]

def test_create(mocker):
  mock_id = mocker.patch("usdm_excel.id_manager.build_id")

  mock_id.side_effect=[f"Code_{x}" for x in range(100)]
  expected_1 = Code(id='Code_1', code='C12345', codeSystem='CDISC', codeSystemVersion='1', decode="Y")
  expected_2 = Code(id='Code_2', code='C12345', codeSystem='CDISC', codeSystemVersion='1', decode="BBB")
  expected_3 = Code(id='Code_3', code='C12345', codeSystem='CDISC', codeSystemVersion='1', decode="1234")
  expected_4 = Code(id='Code_4', code='C12345', codeSystem='CDISC', codeSystemVersion='1', decode="3456")
  expected_5 = Code(id='Code_4', code='C12345', codeSystem='CDISC', codeSystemVersion='1', decode="3456")

  mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
  mock_code.side_effect=[expected_1, expected_2, expected_3, expected_4, expected_5]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [
    # name     description    label          codes                role                type      pharmacologicalClass  productDesignation      minimumResponseDuration,  administrationName [10] administrationDescription administrationLabel administrationRoute administrationDose administrationFrequency administrationDurationDescription administrationDurationWillVary administrationDurationWillVaryReason administrationDurationQuantity
    [ 'Int 1', 'Int Desc 1',  'Int Label 1', 'SPONSOR: A=B',      'M11: role1=role1', 'C12345', 'FDA: A=B',           'M11: desig1=desig_1',  '1 Day',                  'Admin 1',              'Admin Desc 1',           'Admin Label 1',    'C34567',          '12 mg',            'C65432',               'Dur desc 1',                     'False',                       '',                                  '14 %'                         ], 
    [ '',      '',            '',            '',                  '',                 '',       '',                   '',                     '',                       'Admin 2',              'Admin Desc 2',           'Admin Label 1',    'C34567',          '1 mg',             'C65432',               'Dur desc 1',                     'False',                       '',                                  '10 m'                         ], 
    [ 'Int 2', 'Int Desc 2',  'Int Label 2', 'SPONSOR: C=D',      'M11: role2=role2', 'C12345', 'FDA: A=B',           'M11: desig2=desig_2',  '3 Weeks',                'Admin 3',              'Admin Desc 3',           'Admin Label 1',    'C34567',          '100 mg',           'C65432',               'Dur desc 1',                     'False',                       '',                                  '12 C'                         ], 
    [ 'Int 3', 'Int Desc 3',  'Int Label 3', 'SPONSOR: E=F, G=H', 'M11: role3=role3', 'C12345', 'FDA: A=B',           'M11: desig3=desig_3',  '4 Years',                'Admin 4',              'Admin Desc 4',           'Admin Label 1',    'C34567',          '500 mg',           'C65432',               'Dur desc 1',                     'False',                       '',                                  '12 F'                         ], 
    [ '',      '',            '',            '',                  '',                 '',       '',                   '',                     '',                       'Admin 5',              'Admin Desc 5',           'Admin Label 1',    'C34567',          '1 mg',             'C65432',               'Dur desc 1',                     'False',                       '',                                  '15 in'                        ], 
  ]
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=COLUMNS)
  Interventions = StudyDesignInterventionSheet("")
  assert len(Interventions.items) == 3
  assert Interventions.items[0].id == 'InterventionId_1'
  assert Interventions.items[0].name == 'Intervention 1'
  assert Interventions.items[1].id == 'InterventionId_2'
  assert Interventions.items[1].description == 'Intervention Two'
  assert Interventions.items[1].codes == [expected_2]
  assert Interventions.items[2].id == 'InterventionId_3'
  assert Interventions.items[2].codes == [expected_3, expected_4]
  
def test_create_empty(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=COLUMNS)
  Interventions = StudyDesignInterventionSheet("")
  assert len(Interventions.items) == 0

def test_read_cell_by_name_error(mocker):
  mock_error = mocker.patch("usdm_excel.errors.errors.Errors.add")
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = [['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']]
  mock_read = mocker.patch("pandas.read_excel")
  columns = COLUMNS
  columns = columns[0:-1]
  mock_read.return_value = pd.DataFrame(data, columns=columns)
  Interventions = StudyDesignInterventionSheet("")
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == "studyDesignInterventions"
  assert mock_error.call_args[0][1] == None
  assert mock_error.call_args[0][2] == None
  assert mock_error.call_args[0][3] == "Exception ['codes'] raised reading sheet."
  
