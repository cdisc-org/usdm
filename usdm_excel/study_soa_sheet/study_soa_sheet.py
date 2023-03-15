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
      self.activities = []
      self.timelines = []
      self.biomedical_concept_surrogates = []
      self.biomedical_concepts = []
      self._raw_cycles = Cycles(self.sheet, self.id_manager)
      self._raw_timepoints = Timepoints(self.sheet, self.id_manager)
      self._raw_encounters = Encounters(self.sheet, self.id_manager)
      self._raw_activities = Activities(self.sheet, self.id_manager)

      self._link_instance_to_encounter()
      self._link_instance_to_activities()
      self._insert_cycles_into_timeline()
      self._raw_timepoints.set_condition_refs()

      instances = []
      for item in self._raw_encounters.items:
        self.encounters.append(item.usdm_encounter)
      self.double_link(self.encounters, 'encounterId', 'previousEncounterId', 'nextEncounterId')

      for item in self._raw_activities.items:
        self.activities.append(item.usdm_activity)
        self.biomedical_concept_surrogates += item.usdm_biomedical_concept_surrogates
        self.biomedical_concepts += item.usdm_biomedical_concepts
      self.double_link(self.activities, 'activityId', 'previousActivityId', 'nextActivityId')
      
      for raw_timepoint in self._raw_timepoints.items:
        instance = raw_timepoint.usdm_timepoint
        instances.append(instance)
      exit = self._add_exit()
      self.timelines.append(self._add_timeline('Main Timeline', 'This is the main timeline for the study design.', 'Potential subject identified', instances, exit))

    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()

  def epoch_encounter_map(self, epoch):
    return self._raw_encounters.epoch_encounter_map(epoch)
  
  def _add_exit(self):
    return ScheduleTimelineExit(scheduleTimelineExitId=self.id_manager.build_id(ScheduleTimelineExit))

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
    for timepoint in self._raw_timepoints.items:
      if timepoint.has_encounter:
        encounter = self._raw_encounters.item_at(timepoint.key())
        timepoint.add_encounter(encounter)
  
  def _link_instance_to_activities(self):
    for timepoint in self._raw_timepoints.items:
      if timepoint.has_encounter:
        for activity_name, selected in timepoint.activity_map.items():
          if selected:
            activity = self._raw_activities.item_by_name(activity_name)
            timepoint.add_activity(activity)

  def _insert_cycles_into_timeline(self):
    cycle_offset = 0
    for cycle in self._raw_cycles.items:
      start_index = cycle.start_timepoint_index + cycle_offset
      self._raw_timepoints.insert_at(start_index, 'anchor', cycle.start, cycle.cycle)
      cycle_offset += 1

      end_index = cycle.end_timepoint_index + cycle_offset + 1
      self._raw_timepoints.insert_at(end_index, 'previous', cycle.period, None)
      cycle_offset += 1

      if cycle.end_rule != "":
        end_index = cycle.end_timepoint_index + cycle_offset + 1
        self._raw_timepoints.insert_at(end_index, 'condition', cycle.end_rule, None, start_index)
        cycle_offset += 1

