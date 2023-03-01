from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import IdManager
from usdm_excel.cdisc import CDISC
from usdm.timing import Timing
from usdm.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
import pandas as pd

class Timepoint(BaseSheet):
  
  def __init__(self, sheet, id_manager: IdManager, activity_names, col_index, type="", value="", cycle=None, additional=False):
    super().__init__(sheet, id_manager)
    self.col_index = col_index
    self._position_key = col_index - SoAColumnRows.FIRST_VISIT_COL
    self.has_encounter = not additional
    self.activities = []
    self.activity_map = {}
    self.timing_type = type
    self.timing_value = value
    self.reference = None
    self.cycle = cycle
    if not additional:
      self._process_timepoint()
      self._add_activities(activity_names)
    self.usdm_timepoint = self._as_usdm()

  def key(self):
    return self._position_key
  
  def add_encounter(self, encounter):
    self.usdm_timepoint.scheduledInstanceEncounterId = encounter.usdm_encounter.encounterId

  def add_activity(self, activity):
    self.usdm_timepoint.activityIds.append(activity.usdm_activity.activityId)

  def _process_timepoint(self):
    rel_ref = 0
    timing_info, timing_info_is_null = self.clean_cell_unnamed_new(SoAColumnRows.TIMING_ROW, self.col_index)
    if not timing_info_is_null:
      timing_parts = timing_info.split(":")
      if timing_parts[0].upper()[0] == "A":
        self.timing_type = "anchor"
        rel_ref = 0
      if timing_parts[0].upper()[0] == "P":
        self.timing_type = "previous"
        rel_ref = self.get_relative_ref(timing_parts[0]) * -1
      elif timing_parts[0].upper()[0] == "N":
        self.timing_type = "next"
        rel_ref = self.get_relative_ref(timing_parts[0])
      elif timing_parts[0].upper()[0] == "C":
        self.timing_type = "cycle start"
        rel_ref = self.get_relative_ref(timing_parts[0])
      if len(timing_parts) == 2:
        self.timing_value = timing_parts[1].strip()
    self.reference = self.col_index - SoAColumnRows.FIRST_VISIT_COL + rel_ref

  def _as_usdm(self):
    timing = self._to_timing()
    instance = ScheduledActivityInstance(
      scheduledInstanceId=self.id_manager.build_id(ScheduledActivityInstance),
      scheduledInstanceType=1,
      scheduleSequenceNumber=0,
      scheduleTimelineExitId="",
      scheduledInstanceEncounterId="",
      scheduledInstanceTimings=[timing],
      scheduledInstanceTimelineId="",
      activityIds=[]
    )
    timing.relativeFromScheduledInstanceId = instance.scheduledInstanceId
    return instance

  # def _as_usdm_timing(self):
  #   # if self.timing_type == 'next':
  #   #   self.timing = self._add_timing(self.json_engine.add_next_timing(timepoint['value'], 'StartToStart', None, tps[timepoint['ref']]['timepointId']))
  #   # elif self.timing_type == 'previous':
  #   #   timing.append(self.json_engine.add_previous_timing(timepoint['value'], 'StartToStart', None, tps[timepoint['ref']]['timepointId']))
  #   # elif self.timing_type == 'anchor':
  #   #   timing.append(self.json_engine.add_anchor_timing(timepoint['value'], timepoint['cycle']))
  #   # elif self.timing_type == 'condition':
  #   #   #timing.append(self.json_engine.add_condition_timing(timepoint['value']))
  #   #   timing.append({})
  #   # elif self.timing_type == 'cycle start':
  #   #   timing.append(self.json_engine.add_cycle_start_timing(timepoint['value']))
  #   # elif self.timing_type == '':
  #   #   timing.append({})
  #   return self._to_timing()
  
  def _to_timing(self):
    cdisc = CDISC(self.id_manager)
    return Timing(
      timingId=self.id_manager.build_id(Timing),
      timingType=cdisc.code(self.timing_type.upper(), self.timing_type),
      timingValue=self.timing_value,
      timingRelativeToFrom=cdisc.code('START TO START', 'Start to start'),
      timingWindow='',
      relativeFromScheduledInstanceId='',
      relativeToScheduledInstanceId=''
    )

  def get_relative_ref(self, part):
    if len(part) > 1:
      return int(part[1:])
    else:
      return 1

  def _add_activities(self, activity_names):
    for activity in activity_names:
      self.activity_map[activity] = False
    column = self.sheet.iloc[:, self.col_index]
    row = 0
    for cell in column:
      if row >= SoAColumnRows.FIRST_ACTIVITY_ROW:
        activity, activity_is_null = self.clean_cell_unnamed_new(row, SoAColumnRows.CHILD_ACTIVITY_COL)
        if cell.upper() == "X":
          self.activity_map[activity] = True
      row += 1