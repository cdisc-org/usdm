from tests.mocks.mock_general import *
from tests.mocks.mock_sheet import *
from tests.mocks.mock_ids import *
from tests.mocks.mock_logging import *
from usdm_model.study_amendment import StudyAmendment
from usdm_excel.study_amendment_sheet.study_amendment_sheet import StudyAmendmentSheet
from usdm_model.code import Code

def test_create(mocker, globals):

  sheet_data = {
    'number': ['1', '2', '3'], 
    'summary': ['Added section on unblinding', 'Amended Design', 'Fix typos'], 
    'substantialImpact': ['Y', 'Y', 'N'], 
    'primaryReason': ['New Safety Information Available', 'Change In Strategy', 'Other=Fix typographical errors'],
    'secondaryReasons': ['', 'Investigator/Site Feedback', ''],
    'enrollment': ['Region: Europe=15, Country: USA=20%', 'Global:31%', 'Region: Europe=0'],
  }
  index = 1
  object_data = []
  for y in range(3):
    dcrs = []
    refs = sheet_data['sections'][y]
    for ref in refs.split(','):
      parts = ref.split(':')
      dcr = {'sectionNumber': parts[0].strip(), 'sectionTitle': parts[1].strip()}
      dcrs.append(fake_create_object(DocumentContentReference, dcr, index))
      sc = {'cls': DocumentContentReference, 'data': dcr}
      object_data.append(sc)    
      index += 1
    sc = {'cls': StudyChange, 'data': {'changedSections': dcrs}}
    for x in ['name', 'description', 'label', 'rationale', 'summary']:
      sc['data'][x] = sheet_data[x][y]
    object_data.append(sc)
  mock_create_object(mocker, object_data)
  mock_sheet_present(mocker)
  mock_sheet(mocker, globals, sheet_data)
  item = StudyAmendmentSheet("", globals)
  assert len(item.items) == 3
  assert item.items[0].model_dump() == {
    'id': 'StudyChange_2',
    'description': 'Change Desc One',
    'instanceType': 'StudyChange',
    'label': 'Change Label One',
    'name': 'Change One',
    'rationale': 'R1',
    'summary': 'Summary 1',
    'changedSections': [
      {
        'id': 'DocumentContentReference_1',
        'instanceType': 'DocumentContentReference',
        'sectionNumber': '1.2.1',
        'sectionTitle': 'XXX',
      },
    ]
  }
  assert item.items[1].model_dump() == {
    'id': 'StudyChange_5',
    'description': 'Change Desc Two',
    'instanceType': 'StudyChange',
    'label': 'Change Label Two',
    'name': 'Change Two',
    'rationale': 'R2',
    'summary': 'Summary 2',
    'changedSections': [
      {
        'id': 'DocumentContentReference_2',
        'instanceType': 'DocumentContentReference',
        'sectionNumber': '1.3.1',
        'sectionTitle': 'YYY',
      },
      {
        'id': 'DocumentContentReference_3',
        'instanceType': 'DocumentContentReference',
        'sectionNumber': '3.2',
        'sectionTitle': 'ZZZ',
      },
    ]
  }
  assert item.items[2].model_dump() == {
    'id': 'StudyChange_7',
    'description': 'Change Desc Three',
    'instanceType': 'StudyChange',
    'label': 'Change Label Three',
    'name': 'Change Three',
    'rationale': 'R3',
    'summary': 'Summary 3',
    'changedSections': [
      {
        'id': 'DocumentContentReference_4',
        'instanceType': 'DocumentContentReference',
        'sectionNumber': '4.5',
        'sectionTitle': 'Something Long',
      },
    ]
  }
  
def test_create_empty(mocker, globals):
  sheet_data = {}
  mock_sheet_present(mocker)
  mock_sheet(mocker, globals, sheet_data)
  item = StudyAmendmentSheet("", globals)
  assert len(item.items) == 0

def test_read_cell_by_name_error(mocker, globals):
  sheet_data = {
    'amendment': ['A1'], 
    'name': ['Change One'], 
    'description': ['Change Desc One'], 
    'label': ['Change Label One'],
    'summary': ['Summary 1'],
    'sections': ['1.2.1: XXX']
  }
  mea = mock_error_add(mocker, [None, None, None, None, None, None])
  mock_sheet_present(mocker)
  mock_sheet(mocker, globals, sheet_data)
  item = StudyAmendmentSheet("", globals)
  assert mock_called(mea, 2)
  mock_parameters_correct(mea, [mocker.call('amendmentChanges', 1, -1, "Error attempting to read cell 'rationale'. Exception: Failed to detect column(s) 'rationale' in sheet", 40), 
                                mocker.call('amendmentChanges', 1, 1, "Failed to find amendment 'A1'", 40)])
