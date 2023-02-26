from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import IdManager
from usdm_excel.study_soa_sheet.cycles import Cycles
from usdm_excel.study_soa_sheet.timepoints import Timepoints
from usdm_excel.study_soa_sheet.encounters import Encounters
from usdm_excel.study_soa_sheet.activities import Activities
from usdm.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
from usdm.schedule_timeline import ScheduleTimeline

import traceback
import pandas as pd

class StudySoASheet(BaseSheet):

  def __init__(self, file_path, id_manager: IdManager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='soa', header=None), id_manager)
      self.timelines = []
      #self.epoch_encounter_map = {}
      #self.activity_map = {}
      self.row_activities_map = []
      self.activity_bc_map = {}
      self.sheet = self.sheet.fillna(method='ffill', axis=1)
      self.cycles = Cycles(self.id_manager)
      self.timepoints = Timepoints(self.id_manager)
      self.encounters = Encounters(self.id_manager)
      self.activities = Activities(self.id_manager)

      self.process_sheet()
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()

  def process_sheet(self):
    tps = []
    acts = []
    encs = []
    bcs = []
    acts_map = {}
    timing = []
    cycle_offset = 0
    
    # for index, timepoint in enumerate(self.timepoints):
    #   timepoint['activity_index'] = index
    #   timepoint['encounter_index'] = index
    for cycle in self.cycles.items:
      start_index = cycle['start_index'] + cycle_offset
      self.timepoints.insert(start_index, { 'type': 'anchor', 'ref': 0, 'value': cycle['start'], 'activity_index': None, 'encounter_index': None, 'cycle': cycle['cycle'] })
      cycle_offset += 1
      end_index = cycle['end_index'] + cycle_offset + 1
      self.timepoints.insert(end_index, { 'type': 'previous', 'ref': end_index - 1, 'value': cycle['period'], 'activity_index': None, 'encounter_index': None, 'cycle': None })
      cycle_offset += 1
      end_index = cycle['end_index'] + cycle_offset + 1
      self.timepoints.insert(end_index, { 'type': 'condition', 'ref': start_index , 'value': cycle['end_rule'], 'activity_index': None, 'encounter_index': None, 'cycle': None })
      cycle_offset += 1
    previous_tp_id = None
    for activity in self.activities:
      a_bcs = []
      if activity in self.activity_bc_map:
        for a in self.activity_bc_map[activity]['bc']:
          bc = self.json_engine.add_biomedical_concept_surrogate(a, a, "")
          a_bcs.append(bc['bcSurrogateId'])
          bcs.append(bc)
      acts.append(self.json_engine.add_activity(activity, activity, False, "", a_bcs))
      acts_map[activity] = acts[-1]['activityId']
    for encounter in self.encounters:
      encs.append(self.json_engine.add_encounter(encounter['label'], encounter['label'], None, None, []))
    for timepoint in self.timepoints:
      activity_ids = []
      encounter_id = None
      if not timepoint['activity_index'] == None:
        source = self.tp_activities[timepoint['activity_index']]
        for k, v in source.items():
          if v:
            activity_ids.append(acts_map[k])
      if not timepoint['encounter_index'] == None:
        encounter_id = encs[timepoint['encounter_index']]['encounterId']
      tps.append(self.json_engine.add_timepoint(previous_tp_id, None, activity_ids, encounter_id))
      previous_tp_id = tps[-1]['timepointId']
    for index, timepoint in enumerate(self.timepoints):
      if timepoint['type'] == 'condition':
        tps[index]['cycleId'] = tps[timepoint['ref']]['timepointId']
        tps[index]['_type'] = 'Condition'
    for timepoint in self.timepoints:
      if timepoint['type'] == 'next':
        timing.append(self.json_engine.add_next_timing(timepoint['value'], 'StartToStart', None, tps[timepoint['ref']]['timepointId']))
      elif timepoint['type'] == 'previous':
        timing.append(self.json_engine.add_previous_timing(timepoint['value'], 'StartToStart', None, tps[timepoint['ref']]['timepointId']))
      elif timepoint['type'] == 'anchor':
        timing.append(self.json_engine.add_anchor_timing(timepoint['value'], timepoint['cycle']))
      elif timepoint['type'] == 'condition':
        #timing.append(self.json_engine.add_condition_timing(timepoint['value']))
        timing.append({})
      elif timepoint['type'] == 'cycle start':
        timing.append(self.json_engine.add_cycle_start_timing(timepoint['value']))
      elif timepoint['type'] == '':
        timing.append({})
    for index, tp in enumerate(tps):
      tp['scheduledAt'] = timing[index]
    entry = self.json_engine.add_entry('Main timeline', tps[0]['timepointId'])
    exit = self.json_engine.add_exit()
    tps[-1]['exit'] = exit
    self.timelines.append(self.json_engine.add_timeline(entry, tps, exit))

  def _add_timeline(self, name, description, condition):
    return ScheduleTimeline(
      scheduleTimelineId=self.id_manager.build_id(ScheduleTimeline),
      scheduleTimelineName=name,
      scheduleTimelineDescription=description,
      entryCondition=condition,
      scheduleTimelineEntryId="",
      scheduleTimelineExits=[],
      scheduleTimelineInstances=[]
    )
  
  