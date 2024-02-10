#from usdm_excel.cross_ref import cross_references
#from usdm_excel.id_manager import id_manager
import pandas as pd
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.document.soa import SoA
from usdm_model.activity import Activity
from usdm_model.study_epoch import StudyEpoch
from usdm_model.study_cell import StudyCell
from usdm_model.study_arm import StudyArm
from usdm_model.encounter import Encounter
from usdm_model.study_design import StudyDesign
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_model.scheduled_instance import ScheduledActivityInstance
from usdm_model.schedule_timeline_exit import ScheduleTimelineExit

from tests.test_factory import Factory

cdisc_ct = CDISCCT()
factory = Factory()

dummy_code = cdisc_ct.code("C12345", "decode")

def double_link(items, prev, next):
  for idx, item in enumerate(items):
    if idx == 0:
      setattr(item, prev, None)
    else:
      the_id = getattr(items[idx-1], 'id')
      setattr(item, prev, the_id)
    if idx == len(items)-1:  
      setattr(item, next, None)
    else:
      the_id = getattr(items[idx+1], 'id')
      setattr(item, next, the_id)

def create_activities():
  item_list = [
    {'name': 'A1', 'label': 'Activity 1', 'description': '', 'definedProcedures': [], 'biomedicalConceptIds': [], 'bcCategoryIds': [], 'bcSurrogateIds': [], 'timelineId': None},
    {'name': 'A2', 'label': 'Activity 2', 'description': '', 'definedProcedures': [], 'biomedicalConceptIds': [], 'bcCategoryIds': [], 'bcSurrogateIds': [], 'timelineId': None},
    {'name': 'A3', 'label': 'Activity 3', 'description': '', 'definedProcedures': [], 'biomedicalConceptIds': [], 'bcCategoryIds': [], 'bcSurrogateIds': [], 'timelineId': None},
    {'name': 'A4', 'label': 'Activity 4', 'description': '', 'definedProcedures': [], 'biomedicalConceptIds': [], 'bcCategoryIds': [], 'bcSurrogateIds': [], 'timelineId': None},
    {'name': 'A5', 'label': 'Activity 5', 'description': '', 'definedProcedures': [], 'biomedicalConceptIds': [], 'bcCategoryIds': [], 'bcSurrogateIds': [], 'timelineId': None}
  ]
  results = factory.set(Activity, item_list)
  double_link(results, 'previousId', 'nextId')
  return results

def create_epochs():
  item_list = [
    {'name': 'EP1', 'label': '', 'description': '', 'type': dummy_code},
  ]
  results = factory.set(StudyEpoch, item_list)
  double_link(results, 'previousId', 'nextId')
  return results

def create_encounters():
  item_list = [
    {'name': 'E1', 'label': '', 'description': '', 'type': dummy_code, 'environmentalSetting': [], 'contactModes': [], 'transitionStartRule': None, 'transitionEndRule': None, 'scheduledAtId': None},
    {'name': 'E2', 'label': '', 'description': '', 'type': dummy_code, 'environmentalSetting': [], 'contactModes': [], 'transitionStartRule': None, 'transitionEndRule': None, 'scheduledAtId': None},
    {'name': 'E3', 'label': '', 'description': '', 'type': dummy_code, 'environmentalSetting': [], 'contactModes': [], 'transitionStartRule': None, 'transitionEndRule': None, 'scheduledAtId': None}
  ]
  results = factory.set(Encounter, item_list)
  double_link(results, 'previousId', 'nextId')
  return results

def create_activity_instances():
  item_list = [
    {'timelineExitId': None, 'encounterId': None, 'scheduledInstanceTimelineId': None, 'defaultConditionId': None, 'epochId': None, 'activityIds': []},
    {'timelineExitId': None, 'encounterId': None, 'scheduledInstanceTimelineId': None, 'defaultConditionId': None, 'epochId': None, 'activityIds': []},
    {'timelineExitId': None, 'encounterId': None, 'scheduledInstanceTimelineId': None, 'defaultConditionId': None, 'epochId': None, 'activityIds': []}
  ]
  results = factory.set(ScheduledActivityInstance, item_list)
  results[0].defaultConditionId = results[1].id
  results[1].defaultConditionId = results[2].id
  return results

def scenario_1():
  dummy_cell = factory.item(StudyCell, {'armId': "X", 'epochId': "Y"})
  dummy_arm = factory.item(StudyArm, {'name': "Arm1", 'type': dummy_code, 'dataOriginDescription': 'xxx', 'dataOriginType': dummy_code})
  activities = create_activities()
  epochs = create_epochs()
  encounters = create_encounters()
  activity_instances = create_activity_instances()

  activity_instances[0].activityIds = [activities[0].id, activities[1].id]
  activity_instances[0].encounterId = encounters[0].id
  activity_instances[1].activityIds = [activities[1].id, activities[2].id]
  activity_instances[1].encounterId = encounters[1].id
  activity_instances[2].activityIds = [activities[2].id, activities[3].id, activities[4].id]
  activity_instances[2].encounterId = encounters[2].id

  exit = factory.item(ScheduleTimelineExit, {})
  activity_instances[-1].timelineExitId = exit.id
  timeline = factory.item(ScheduleTimeline, {'name': 'Study Design', 'label': '', 'description': '', 'mainTimeline': True, 'entryCondition': "Condition", 'entryId': activity_instances[0].id, 'exits': [exit], 'instances': activity_instances})
  study_design = factory.item(StudyDesign, {'name': 'Study Design', 'label': '', 'description': '', 
    'rationale': 'XXX', 'interventionModel': dummy_code,
    'arms': [dummy_arm], 'studyCells': [dummy_cell], 'epochs': epochs,
    'activities': activities, 'scheduledTimelines': [timeline]})
  return study_design, timeline

def fake_sheet(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=[])
  return BaseSheet("", "")

def test_create(mocker):
  bs = fake_sheet(mocker)
  study_design, timeline = scenario_1()
  soa = SoA(bs, study_design, timeline)
  result = soa.simple()
  assert result == [
    ['',           0,             1,             2], 
    ['',           'Encounter_1', 'Encounter_2', 'Encounter_3'], 
    ['Activity 1', 'X',           '',            ''], 
    ['Activity 2', 'X',           'X',           ''], 
    ['Activity 3', '',            'X',           'X'], 
    ['Activity 4', '',            '',            'X'], 
    ['Activity 5', '',            '',            'X']
  ]
