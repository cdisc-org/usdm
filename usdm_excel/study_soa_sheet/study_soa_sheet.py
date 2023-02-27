from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import IdManager
from usdm_excel.study_soa_sheet.cycles import Cycles
from usdm_excel.study_soa_sheet.timepoints import Timepoints
from usdm_excel.study_soa_sheet.timepoint import Timepoint
from usdm_excel.study_soa_sheet.encounters import Encounters
from usdm_excel.study_soa_sheet.activities import Activities
from usdm.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
from usdm.schedule_timeline import ScheduleTimeline
from usdm.schedule_timeline_exit import ScheduleTimelineExit

import traceback
import pandas as pd

class StudySoASheet(BaseSheet):

  def __init__(self, file_path, id_manager: IdManager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='soa', header=None), id_manager)
      self.timelines = []
      #self.sheet = self.sheet.fillna(method='ffill', axis=1)
      self.encounters = []
      self.timelines = []
      self.raw_cycles = Cycles(self.sheet, self.id_manager)
      self.raw_timepoints = Timepoints(self.sheet, self.id_manager)
      self.raw_encounters = Encounters(self.sheet, self.id_manager)
      self.raw_activities = Activities(self.sheet, self.id_manager)

      self._link_instance_to_encounter()
      self._link_instance_to_activities()
      self._insert_cycles_into_timeline()

      self.process_sheet()

    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()

  def process_sheet(self):
    timing = []
    instances = []
    for raw_encounter in self.raw_encounters.items:
      self.encounters.append(raw_encounter.as_usdm())
    for raw_timepoint in self.raw_timepoints.items:
      instance = raw_timepoint.as_usdm()
      instances.append(instance)
      timing.append(raw_timepoint.as_usdm_timing())
    exit = self._add_exit()
    self.timelines.append(self._add_timeline('Main Timeline', 'This is the main timeline for the study design.', 'Subject identifier', instances, exit))

  def _add_exit(self):
    return ScheduleTimelineExit(exitId=self.id_manager.build_id(ScheduleTimelineExit))

  def _add_timeline(self, name, description, condition, instances, exit):
    return ScheduleTimeline(
      scheduleTimelineId=self.id_manager.build_id(ScheduleTimeline),
      scheduleTimelineName=name,
      scheduleTimelineDescription=description,
      entryCondition=condition,
      scheduleTimelineEntryId=instances[0].scheduledInstanceId,
      scheduleTimelineExits=[exit],
      scheduleTimelineInstances=instances
    )

  def _link_instance_to_encounter(self):
    for timepoint in self.raw_timepoints.items:
      if timepoint.encounter:
        encounter = self.encounters.item_at(self.raw_timepoints.item_at(timepoint.position_key))
        timepoint.add_encounter(encounter)
  
  def _link_instance_to_activities(self):
    for timepoint in self.raw_timepoints.items:
      if timepoint.encounter:
        for activity_name in timepoint.activities:
          activity = self.raw_activities.item_at_name(activity_name)
          timepoint.add_activity(activity)

  def _insert_cycles_into_timeline(self):
    cycle_offset = 0
    for cycle in self.raw_cycles.items:
      start_index = cycle['start_index'] + cycle_offset
      
      timepoint = Timepoint(self.sheet, self.id_manager, self.activity_names, self.col_index, 'anchor', cycle['start'], cycle['cycle'], additional=True)
      self.raw_timepoints.insert(start_index, timepoint)
      #self.raw_timepoints.insert(start_index, { 'type': 'anchor', 'ref': 0, 'value': cycle['start'], 'activity_index': None, 'encounter_index': None, 'cycle': cycle['cycle'] })

      cycle_offset += 1
      end_index = cycle['end_index'] + cycle_offset + 1
      
      timepoint = Timepoint(self.sheet, self.id_manager, self.activity_names, self.col_index, 'previous', cycle['period'], None, additional=True)
      self.raw_timepoints.insert(start_index, timepoint)
      #self.raw_timepoints.insert(end_index, { 'type': 'previous', 'ref': end_index - 1, 'value': cycle['period'], 'activity_index': None, 'encounter_index': None, 'cycle': None })

      cycle_offset += 1
      end_index = cycle['end_index'] + cycle_offset + 1
      
      timepoint = Timepoint(self.sheet, self.id_manager, self.activity_names, self.col_index, 'condition', cycle['end_rule'], None, additional=True)
      self.raw_timepoints.insert(start_index, timepoint)
      #self.raw_timepoints.insert(end_index, { 'type': 'condition', 'ref': start_index , 'value': cycle['end_rule'], 'activity_index': None, 'encounter_index': None, 'cycle': None })
      
      cycle_offset += 1

