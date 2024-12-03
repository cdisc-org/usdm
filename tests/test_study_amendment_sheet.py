from tests.mocks.mock_general import *
from tests.mocks.mock_sheet import *
from tests.mocks.mock_ids import *
from tests.mocks.mock_logging import *
from usdm_excel.study_amendment_sheet.study_amendment_sheet import StudyAmendmentSheet
from usdm_excel.option_manager import Options, EmptyNoneOption

def test_create(mocker, globals):
  globals.id_manager.clear()
  globals.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.NONE.value)
  sheet_data = {
    'number': ['1', '2'], 
    'summary': ['Added section on unblinding', 'Amended Design'], 
    'primaryReason': ['New Safety Information Available', 'Change In Strategy'],
    'secondaryReasons': ['', 'Investigator/Site Feedback'],
    'enrollment': ['Region: Europe=15, Country: USA=20%', 'Global:31%'],
    'date': ['', '']
  }
  mock_sheet_present(mocker)
  mock_sheet(mocker, globals, sheet_data)
  mock_json = mocker.patch("json.load")
  mock_json.side_effect=[{}, {}, {}]
  item = StudyAmendmentSheet("", globals)
  assert len(item.items) == 2
  assert item.items[0].model_dump() == {
    'id': 'StudyAmendment_1', 
    'number': '1', 
    'summary': 'Added section on unblinding', 
    'primaryReason': {
      'id': 'StudyAmendmentReason_1', 
      'code': {'id': 'Code_1', 'code': 'C99904x4', 'codeSystem': 'http://www.cdisc.org', 'codeSystemVersion': '2023-12-15', 'decode': 'New Safety Information Available', 'instanceType': 'Code'}, 
      'otherReason': None, 
      'instanceType': 'StudyAmendmentReason'
    }, 
    'secondaryReasons': [], 
    'changes': [], 
    'impacts': [], 
    'geographicScopes': [
      {
        'id': 'GeographicScope_3', 
        'type': {'id': 'Code_7', 'code': 'C68846', 'codeSystem': 'http://www.cdisc.org', 'codeSystemVersion': '2023-12-15', 'decode': 'Global', 'instanceType': 'Code'}, 
        'code': None, 
        'instanceType': 'GeographicScope'
      }
    ], 
    'enrollments': [
      {
        'id': 'SubjectEnrollment_1', 
        'name': 'XXX', 
        'label': None, 
        'description': None, 
        'quantity': {'id': 'Quantity_1', 'value': 15.0, 'unit': None, 'instanceType': 'Quantity'}, 
        'appliesTo': {
          'id': 'GeographicScope_1', 
          'type': {'id': 'Code_3', 'code': 'C41129', 'codeSystem': 'http://www.cdisc.org', 'codeSystemVersion': '2023-12-15', 'decode': 'Region', 'instanceType': 'Code'}, 
          'code': {
            'id': 'AliasCode_1', 
            'standardCode': {'id': 'Code_2', 'code': '150', 'codeSystem': 'ISO 3166 1 alpha3', 'codeSystemVersion': '2020-08', 'decode': 'Europe', 'instanceType': 'Code'}, 
            'standardCodeAliases': [], 
            'instanceType': 'AliasCode'
          }, 
          'instanceType': 'GeographicScope'
        }, 
        'appliesToId': None, 
        'instanceType': 'SubjectEnrollment'
      }, 
      {
        'id': 'SubjectEnrollment_2', 
        'name': 'XXX', 
        'label': None, 
        'description': None, 
        'quantity': {
          'id': 'Quantity_2', 
          'value': 20.0, 
          'unit': {
            'id': 'AliasCode_2', 
            'standardCode': {'id': 'Code_4', 'code': 'C25613', 'codeSystem': 'http://www.cdisc.org', 'codeSystemVersion': '2023-12-15', 'decode': 'Percentage', 'instanceType': 'Code'}, 
            'standardCodeAliases': [], 'instanceType': 'AliasCode'
          }, 
          'instanceType': 'Quantity'
        }, 
        'appliesTo': {
          'id': 'GeographicScope_2', 
          'type': {'id': 'Code_6', 'code': 'C25464', 'codeSystem': 'http://www.cdisc.org', 'codeSystemVersion': '2023-12-15', 'decode': 'Country', 'instanceType': 'Code'}, 
          'code': {
            'id': 'AliasCode_3', 
            'standardCode': {'id': 'Code_5', 'code': 'DNK', 'codeSystem': 'ISO 3166 1 alpha3', 'codeSystemVersion': '2020-08', 'decode': 'Denmark', 'instanceType': 'Code'}, 
            'standardCodeAliases': [], 
            'instanceType': 'AliasCode'
          }, 
          'instanceType': 'GeographicScope'
        }, 
        'appliesToId': None, 
        'instanceType': 'SubjectEnrollment'
      }
    ], 
    'dateValues': [], 
    'previousId': None, 
    'notes': [], 
    'instanceType': 'StudyAmendment'
  }
  assert item.items[1].model_dump() == {
    'id': 'StudyAmendment_2', 
    'number': '2', 
    'summary': 'Amended Design', 
    'primaryReason': {
      'id': 'StudyAmendmentReason_2', 
      'code': {'id': 'Code_8', 'code': 'C99904x7', 'codeSystem': 'http://www.cdisc.org', 'codeSystemVersion': '2023-12-15', 'decode': 'Change In Strategy', 'instanceType': 'Code'}, 
      'otherReason': None, 
      'instanceType': 'StudyAmendmentReason'
    }, 
    'secondaryReasons': [
      {
        'code': {
          'code': 'C99904x10',
          'codeSystem': 'http://www.cdisc.org',
          'codeSystemVersion': '2023-12-15',
          'decode': 'Investigator/Site Feedback',
          'id': 'Code_9',
          'instanceType': 'Code',
        },
        'id': 'StudyAmendmentReason_3',
        'instanceType': 'StudyAmendmentReason',
        'otherReason': None,
      },
    ],
    'changes': [], 
    'impacts': [], 
    'geographicScopes': [
      {
        'id': 'GeographicScope_5', 
        'type': {'id': 'Code_12', 'code': 'C68846', 'codeSystem': 'http://www.cdisc.org', 'codeSystemVersion': '2023-12-15', 'decode': 'Global', 'instanceType': 'Code'}, 
        'code': None, 
        'instanceType': 'GeographicScope'
      }
    ], 
    'enrollments': [
      {
        'id': 'SubjectEnrollment_3', 
        'name': 'XXX', 
        'label': None, 
        'description': None, 
        'quantity': {
          'id': 'Quantity_3', 
          'value': 31.0, 
          'unit': {
            'id': 'AliasCode_4', 
            'standardCode': {'id': 'Code_10', 'code': 'C25613', 'codeSystem': 'http://www.cdisc.org', 'codeSystemVersion': '2023-12-15', 'decode': 'Percentage', 'instanceType': 'Code'}, 
            'standardCodeAliases': [], 'instanceType': 'AliasCode'
          }, 
          'instanceType': 'Quantity'
        }, 
        'appliesTo': {
          'id': 'GeographicScope_4', 
          'type': {'id': 'Code_11', 'code': 'C68846', 'codeSystem': 'http://www.cdisc.org', 'codeSystemVersion': '2023-12-15', 'decode': 'Global', 'instanceType': 'Code'}, 
          'code': None, 
          'instanceType': 'GeographicScope'
        }, 
        'appliesToId': None, 
        'instanceType': 'SubjectEnrollment'
      }
    ], 
    'dateValues': [], 
    'previousId': 'StudyAmendment_1', 
    'notes': [], 
    'instanceType': 'StudyAmendment'
  }
  
def test_create_empty(mocker, globals):
  sheet_data = {}
  mock_sheet_present(mocker)
  mock_sheet(mocker, globals, sheet_data)
  item = StudyAmendmentSheet("", globals)
  assert len(item.items) == 0

def test_read_cell_by_name_error(mocker, globals):
  sheet_data = {
    'number': ['1'], 
    'summary': ['Added section on unblinding'], 
    'primaryReason': ['New Safety Information Available'],
    'enrollment': ['Region: Europe=15, Country: USA=20%'],
    'date': ['']
  }
  mea = mock_error_add(mocker, [None, None, None, None, None, None])
  mock_sheet_present(mocker)
  mock_sheet(mocker, globals, sheet_data)
  item = StudyAmendmentSheet("", globals)
  assert mock_called(mea, 1)
  mock_parameters_correct(mea, [mocker.call('studyAmendments', None, None, "Exception. Error [Failed to detect column(s) 'secondaryReasons' in sheet] while reading sheet 'studyAmendments'. See log for additional details.", 40)])
