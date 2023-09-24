from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.study_soa_v2_sheet.activities import Activities
from usdm_excel.study_soa_v2_sheet.scheduled_instances import ScheduledInstances
#from usdm_model.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_model.schedule_timeline_exit import ScheduleTimelineExit

import traceback

class StudySoAV2Sheet(BaseSheet):

  NAME_ROW = 0
  DESCRIPTION_ROW = 1
  CONDITION_ROW = 2
  PARAMS_DATA_COL = 1

  def __init__(self, file_path, sheet_name, main=False, require={}):
    try:
      super().__init__(file_path=file_path, sheet_name=sheet_name, header=None, require=require)
      self.name = ""
      self.description = ""
      self.condition = ""
      self.timeline = None
      self.main_timeline = main
      self.encounters = []
      self.activities = []
      self.timelines = []
      self.biomedical_concept_surrogates = []
      self.biomedical_concepts = []
      self._process_sheet()
      self._raw_instances = ScheduledInstances(self)
      self._raw_activities = Activities(self)

      # @TODO Move block to Activities class
      for item in self._raw_activities.items:
        activity = item.usdm_activity
        self.activities.append(activity)
        self.biomedical_concept_surrogates += item.usdm_biomedical_concept_surrogates
        self.biomedical_concepts += item.usdm_biomedical_concepts
      self.double_link(self.activities, 'previousActivityId', 'nextActivityId')
      
      self.timeline = self._add_timeline(self.name, self.description, self.condition, self._raw_instances.instances, self._raw_instances.exits)

    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet")
      self._traceback(f"{traceback.format_exc()}")

  def set_timing_references(self, timings):
    #print(f"TR1:")
    for timing in timings:
      #print(f"TR2: {timing}")
      instance = self._raw_instances.match(timing.relativeFromScheduledInstanceId)
      #print(f"TR3: {instance}")
      if instance:
        item = instance.item
        #print(f"TR4: {item}")
        timing.relativeFromScheduledInstanceId = item.id
        item.scheduledInstanceTimings.append(timing)
      else:
        self._general_error(f"Unable to find timing 'from' reference with name {timing.relativeFromScheduledInstanceId}")
      instance = self._raw_instances.match(timing.relativeToScheduledInstanceId)
      #print(f"TR5: {instance}")
      if instance:
        item = instance.item
        #print(f"TR6: {item}")
        timing.relativeToScheduledInstanceId = item.id
      else:
        self._general_error(f"Unable to find timing 'to' reference with name {timing.relativeToScheduledInstanceId}")
      
  def _process_sheet(self):
    for rindex in range(self.NAME_ROW, self.CONDITION_ROW + 1):
      if rindex == self.NAME_ROW:
        self.name = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.DESCRIPTION_ROW:
        self.description = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.CONDITION_ROW:
        self.condition = self.read_cell(rindex, self.PARAMS_DATA_COL)
      else:
        pass

  def _add_timeline(self, name, description, condition, instances, exit):
    timeline = ScheduleTimeline(
      id=id_manager.build_id(ScheduleTimeline),
      mainTimeline=self.main_timeline,
      name=name,
      description=description,
      label=name,
      entryCondition=condition,
      scheduleTimelineEntryId=instances[0].id,
      scheduleTimelineExits=exit,
      scheduleTimelineInstances=instances
    )
    cross_references.add(timeline.id, timeline)
    return timeline




