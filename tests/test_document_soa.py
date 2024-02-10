#from src.usdm_excel.cross_ref import cross_references
#from src.usdm_excel.id_manager import id_manager
from src.usdm_excel.base_sheet import BaseSheet
from src.usdm_excel.cdisc_ct import CDISCCT
from src.usdm_excel.document.soa import SoA
from src.usdm_model.activity import Activity
from src.usdm_model.study_epoch import StudyEpoch
from src.usdm_model.encounter import Encounter
from src.usdm_model.study_design import StudyDesign
from src.usdm_model.schedule_timeline import ScheduleTimeline

from tests.test_factory import Factory

bs = BaseSheet
cdisc_ct = CDISCCT()
factory = Factory()

dummy_code = cdisc_ct.code("C12345", "decode")

def create_activities():
  item_list = [
    {'name': 'A1', 'label': '', 'description': '', 'definedProcedures': [], 'biomedicalConceptIds': [], 'bcCategoryIds': [], 'bcSurrogateIds': [], 'timelineId': None}
  ]
  results = factory.set(Activity, item_list)
  bs.double_link(results, 'previousId', 'nextId')
  return results

def create_epochs():
  item_list = [
    {'name': 'EP1', 'label': '', 'description': '', 'type': dummy_code},
  ]
  results = factory.set(StudyEpoch, item_list)
  bs.double_link(results, 'previousId', 'nextId')
  return results

def create_encounters():
  item_list = [
    {'name': 'E1', 'label': '', 'description': '', 'type': dummy_code, 'environmentalSetting': [], 'contactModes': [], 'transitionStartRule': None, 'transitionEndRule': None, 'scheduledAtId': None},
  ]
  results = factory.set(Encounter, item_list)
  bs.double_link(results, 'previousId', 'nextId')
  return results

def create_activity_instance():
  item_list = [
    {'timelineExitId': None, 'encounterId': None, 'scheduledInstanceTimelineId': None, 'defaultConditionId': None, 'epochId': None, 'activityIds': []}
  ]
  results = factory.set(Encounter, item_list)
  return results

def scenario_1():
  activities = create_activities()
  epochs = create_epochs()
  encounters = create_encounters()
  activity_instances = create_activity_instance()
  study_design = factory.item(StudyDesign, {'name': 'Study Design', 'label': '', 'description': ''})
  timeline = factory.item(ScheduleTimeline, {'name': 'Study Design', 'label': '', 'description': '', 'mainTimeline': True, 'entryCondition': None, 'entryId': activity_instances[0], 'exits': exit, 'instances': activity_instances})
  return study_design, timeline

def test_create():
  study_design, timeline = scenario_1()
  soa = SoA(bs, study_design, timeline)
  result = soa.simple()
  print(f"SOA: {result}")
