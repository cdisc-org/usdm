import pandas as pd
from typing import List
from usdm_excel.study_design_sheet.study_design_sheet import StudyDesignSheet
from usdm_model.study_arm import StudyArm
from usdm_model.study_epoch import StudyEpoch
from usdm_model.study_element import StudyElement
from usdm_excel.globals import Globals
from tests.test_factory import Factory
from usdm_excel.globals import Globals
from tests.test_factory import Factory

def test_create(mocker, factory: Factory, globals: Globals):
  data = [*zip(
    [
      'studyDesignName',
      'studyDesignDescription',
      'therapeuticAreas',
      'studyDesignRationale',
      'studyDesignBlindingScheme',
      'trialIntentTypes',
      'trialSubTypes',
      'interventionModel',
      'mainTimeline',
      'otherTimelines', # 10
      'studyType',
      'studyPhase',
      'specimenRetentions',
      'timePerspective',
      'samplingMethod',
      'characteristics',
      '',
      'Arms/Epochs', # 18
      'Arm 1',
      'Arm 2'
    ],
    [
      'Study Design 1',
      'The main design for the study',
      'SPONSOR: MILD_MOD_ALZ=Mild to Moderate Alzheimers Disease, SNOMED: 26929004=Alzheimers disease',
      'The discontinuation rate associated with this oral dosing regimen was 58.6% in previous studies, and alternative clinical strategies have been sought to improve tolerance for the compound. To that end, development of a Transdermal Therapeutic System (TTS) has been initiated.',
      'DOUBLE BLIND',
      'TREATMENT',
      'Efficacy Study, Safety Study, Pharmacokinetic Study',
      'C82639',
      'mainTimeline',
      'adverseEventTimeline, earlyTerminationTimeline, vsBloodPressure', # 10
      'Interventional',
      'Phase II Trial',
      'Randomised',
      '',
      '',
      '',
      '',
      'Screening', # 18
      'EL1',
      'EL2'
    ],
    [
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '', # 10
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      'Treatment 1', # 17
      'EL2',
      'EL3'
    ],
    [
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      'Follow Up', # 17
      'EL4',
      'EL4'
    ]    
  )]
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=[f"X{i}" for i in range(1, 50)]
  _setup(mocker, globals, data)
  _create_arms_epochs_elements(factory, globals)
  item = StudyDesignSheet("", globals)
  assert len(item.items) == 1
  assert item.items[0].model_dump() == _expected()

def test_create_empty(mocker, globals):
  data = []
  _setup(mocker, globals, data)
  item = StudyDesignSheet("", globals)
  assert len(item.items) == 0

def test_read_cell_by_name_error(mocker, globals):
  data = {
    'name': ['A1'], 
    'description': ['Annotation Text One'],
    'label': ['LABEL1'],
    'includesDNA': [True],
  }
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=['Code_1', 'BiospecimenRetention_1']
  _setup(mocker, globals, data)
  item = StudyDesignSheet("", globals)
  assert mock_error.call_count == 1
  mock_error.assert_has_calls(
    [
      mocker.call('studyDesignSpecimen', 1, -1, "Error attempting to read cell 'retained'. Exception: Failed to detect column(s) 'retained' in sheet", 40),
    ]
  )
  
def _setup(mocker, globals: Globals, data: List[List[str]]):
  globals.cross_references.clear()
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data)

def _create_arms_epochs_elements(factory: Factory, globals: Globals):
  dot = factory.cdisc_code("C12345", "data origin")
  et = factory.cdisc_code("C12346", "epoch type")
  at = factory.cdisc_code("C12347", "arm type")
  arms = [
    {'name': 'Arm 1', 'type': at, 'dataOriginType': dot, 'dataOriginDescription': "data description"},
    {'name': 'Arm 2', 'type': at, 'dataOriginType': dot, 'dataOriginDescription': "data description"}, 
    {'name': 'Arm 3', 'type': at, 'dataOriginType': dot, 'dataOriginDescription': "data description"}
  ]
  for item in arms:
    instance = factory.item(StudyArm, item)
    globals.cross_references.add(item['name'], instance)

  epochs = [
    {'name': 'Screening', 'type': et},
    {'name': 'Treatment 1', 'type': et}, 
    {'name': 'Follow Up', 'type': et}
  ]
  for item in epochs:
    instance = factory.item(StudyEpoch, item)
    globals.cross_references.add(item['name'], instance)

  elements = [
    {'name': 'EL1'},
    {'name': 'EL2'}, 
    {'name': 'EL3'},
    {'name': 'EL4'}
  ]
  for item in elements:
    instance = factory.item(StudyElement, item)
    globals.cross_references.add(item['name'], instance)

def _expected():
  return {
     'activities': [],
     'analysisPopulations': [],
     'arms': [
         {
             'dataOriginDescription': 'data description',
             'dataOriginType': {
                 'code': 'C12345',
                 'codeSystem': 'xxx',
                 'codeSystemVersion': '1',
                 'decode': 'data origin',
                 'id': 'X1',
                 'instanceType': 'Code',
             },
             'description': None,
             'id': 'X4',
             'instanceType': 'StudyArm',
             'label': None,
             'name': 'Arm 1',
             'notes': [],
             'populationIds': [],
             'type': {
                 'code': 'C12347',
                 'codeSystem': 'xxx',
                 'codeSystemVersion': '1',
                 'decode': 'arm type',
                 'id': 'X3',
                 'instanceType': 'Code',
             },
         },
         {
             'dataOriginDescription': 'data description',
             'dataOriginType': {
                 'code': 'C12345',
                 'codeSystem': 'xxx',
                 'codeSystemVersion': '1',
                 'decode': 'data origin',
                 'id': 'X1',
                 'instanceType': 'Code',
             },
             'description': None,
             'id': 'X5',
             'instanceType': 'StudyArm',
             'label': None,
             'name': 'Arm 2',
             'notes': [],
             'populationIds': [],
             'type': {
                 'code': 'C12347',
                 'codeSystem': 'xxx',
                 'codeSystemVersion': '1',
                 'decode': 'arm type',
                 'id': 'X3',
                 'instanceType': 'Code',
             },
         },
     ],
     'bcCategories': [],
     'bcSurrogates': [],
     'biomedicalConcepts': [],
     'biospecimenRetentions': [],
     'blindingSchema': {
         'id': 'X17',
         'instanceType': 'AliasCode',
         'standardCode': {
             'code': 'C15228',
             'codeSystem': 'http://www.cdisc.org',
             'codeSystemVersion': '2024-09-27',
             'decode': 'Double Blind Study',
             'id': 'X16',
             'instanceType': 'Code',
         },
         'standardCodeAliases': [],
     },
     'characteristics': [],
     'conditions': [],
     'description': 'The main design for the study',
     'dictionaries': [],
     'documentVersionIds': [],
     'elements': [
         {
             'description': None,
             'id': 'X10',
             'instanceType': 'StudyElement',
             'label': None,
             'name': 'EL1',
             'notes': [],
             'studyInterventionIds': [],
             'transitionEndRule': None,
             'transitionStartRule': None,
         },
         {
             'description': None,
             'id': 'X11',
             'instanceType': 'StudyElement',
             'label': None,
             'name': 'EL2',
             'notes': [],
             'studyInterventionIds': [],
             'transitionEndRule': None,
             'transitionStartRule': None,
         },
         {
             'description': None,
             'id': 'X13',
             'instanceType': 'StudyElement',
             'label': None,
             'name': 'EL4',
             'notes': [],
             'studyInterventionIds': [],
             'transitionEndRule': None,
             'transitionStartRule': None,
         },
         {
             'description': None,
             'id': 'X12',
             'instanceType': 'StudyElement',
             'label': None,
             'name': 'EL3',
             'notes': [],
             'studyInterventionIds': [],
             'transitionEndRule': None,
             'transitionStartRule': None,
         },
     ],
     'encounters': [],
     'epochs': [
         {
             'description': None,
             'id': 'X7',
             'instanceType': 'StudyEpoch',
             'label': None,
             'name': 'Screening',
             'nextId': 'X8',
             'notes': [],
             'previousId': None,
             'type': {
                 'code': 'C12346',
                 'codeSystem': 'xxx',
                 'codeSystemVersion': '1',
                 'decode': 'epoch type',
                 'id': 'X2',
                 'instanceType': 'Code',
             },
         },
         {
             'description': None,
             'id': 'X8',
             'instanceType': 'StudyEpoch',
             'label': None,
             'name': 'Treatment 1',
             'nextId': 'X9',
             'notes': [],
             'previousId': 'X7',
             'type': {
                 'code': 'C12346',
                 'codeSystem': 'xxx',
                 'codeSystemVersion': '1',
                 'decode': 'epoch type',
                 'id': 'X2',
                 'instanceType': 'Code',
             },
         },
         {
             'description': None,
             'id': 'X9',
             'instanceType': 'StudyEpoch',
             'label': None,
             'name': 'Follow Up',
             'nextId': None,
             'notes': [],
             'previousId': 'X8',
             'type': {
                 'code': 'C12346',
                 'codeSystem': 'xxx',
                 'codeSystemVersion': '1',
                 'decode': 'epoch type',
                 'id': 'X2',
                 'instanceType': 'Code',
             },
         },
     ],
     'estimands': [],
     'id': 'X32',
     'indications': [],
     'instanceType': 'InterventionalStudyDesign',
     'intentTypes': [
         {
             'code': 'C49656',
             'codeSystem': 'http://www.cdisc.org',
             'codeSystemVersion': '2024-09-27',
             'decode': 'Treatment Study',
             'id': 'X18',
             'instanceType': 'Code',
         },
     ],
     'label': 'USDM Example Study Design',
     'model': {
         'code': 'C82639',
         'codeSystem': 'http://www.cdisc.org',
         'codeSystemVersion': '2024-09-27',
         'decode': 'Parallel Study',
         'id': 'X22',
         'instanceType': 'Code',
     },
     'name': 'Study Design 1',
     'notes': [],
     'objectives': [],
     'population': None,
     'rationale': 'The discontinuation rate associated with this oral dosing regimen was '
     '58.6% in previous studies, and alternative clinical strategies have been '
     'sought to improve tolerance for the compound. To that end, development of '
     'a Transdermal Therapeutic System (TTS) has been initiated.',
     'scheduleTimelines': [],
     'studyCells': [
         {
             'armId': 'X4',
             'elementIds': [
                 'X10',
             ],
             'epochId': 'X7',
             'id': 'X26',
             'instanceType': 'StudyCell',
         },
         {
             'armId': 'X4',
             'elementIds': [
                 'X11',
             ],
             'epochId': 'X8',
             'id': 'X27',
             'instanceType': 'StudyCell',
         },
         {
             'armId': 'X4',
             'elementIds': [
                 'X13',
             ],
             'epochId': 'X9',
             'id': 'X28',
             'instanceType': 'StudyCell',
         },
         {
             'armId': 'X5',
             'elementIds': [
                 'X11',
             ],
             'epochId': 'X7',
             'id': 'X29',
             'instanceType': 'StudyCell',
         },
         {
             'armId': 'X5',
             'elementIds': [
                 'X12',
             ],
             'epochId': 'X8',
             'id': 'X30',
             'instanceType': 'StudyCell',
         },
         {
             'armId': 'X5',
             'elementIds': [
                 'X13',
             ],
             'epochId': 'X9',
             'id': 'X31',
             'instanceType': 'StudyCell',
         },
     ],
     'studyInterventions': [],
     'studyPhase': {
         'id': 'X25',
         'instanceType': 'AliasCode',
         'standardCode': {
             'code': 'C15601',
             'codeSystem': 'http://www.cdisc.org',
             'codeSystemVersion': '2024-09-27',
             'decode': 'Phase II Trial',
             'id': 'X24',
             'instanceType': 'Code',
         },
         'standardCodeAliases': [],
     },
     'studyType': None,
     'subTypes': [
         {
             'code': 'C49666',
             'codeSystem': 'http://www.cdisc.org',
             'codeSystemVersion': '2024-09-27',
             'decode': 'Efficacy Study',
             'id': 'X19',
             'instanceType': 'Code',
         },
         {
             'code': 'C49667',
             'codeSystem': 'http://www.cdisc.org',
             'codeSystemVersion': '2024-09-27',
             'decode': 'Safety Study',
             'id': 'X20',
             'instanceType': 'Code',
         },
         {
             'code': 'C49663',
             'codeSystem': 'http://www.cdisc.org',
             'codeSystemVersion': '2024-09-27',
             'decode': 'Pharmacokinetic Study',
             'id': 'X21',
             'instanceType': 'Code',
         },
     ],
     'therapeuticAreas': [
         {
             'code': 'MILD_MOD_ALZ',
             'codeSystem': 'SPONSOR',
             'codeSystemVersion': '',
             'decode': 'Mild to Moderate Alzheimers Disease',
             'id': 'X14',
             'instanceType': 'Code',
         },
         {
             'code': '26929004',
             'codeSystem': 'SNOMED',
             'codeSystemVersion': '',
             'decode': 'Alzheimers disease',
             'id': 'X15',
             'instanceType': 'Code',
         },
     ],
 }