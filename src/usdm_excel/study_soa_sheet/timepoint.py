from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.cdisc_ct import CDISCCT
from usdm_model.timing import Timing
from usdm_model.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
#import pandas as pd

class Timepoint():
  
  def __init__(self, parent, activity_names, col_index, type="", value="", cycle=None, additional=False):
    self.parent = parent
    self.col_index = col_index
    if col_index == None:
      self._position_key = None
    else:
      self._position_key = col_index - SoAColumnRows.FIRST_VISIT_COL
    self.encounter_xref = ""
    self.has_activities = not additional
    self.has_encounter = False
    if not additional:
      self.encounter_xref, encounter_is_null = self.parent.read_cell_empty_legacy(SoAColumnRows.VISIT_LABEL_ROW, col_index)
      if not self.encounter_xref == "":
        self.has_encounter = True
      self.epoch = self.parent.read_cell_with_previous(SoAColumnRows.EPOCH_ROW, col_index, SoAColumnRows.FIRST_VISIT_COL)
      epoch_ref = cross_references.get(self.epoch)
    self.activities = []
    self.activity_map = {}
    self.timing_type = type
    self.timing_value = value
    self.window = ''
    self.reference = None
    self.cycle = cycle
    if not additional:
      self._process_timepoint()
      self._add_activities(activity_names)
    self.usdm_timepoint = self._as_usdm()
    if self.has_encounter:
      encounter = cross_references.get(self.encounter_xref)
      self.usdm_timepoint.scheduledActivityInstanceEncounterId = encounter.encounterId
    self.usdm_timepoint.epochId = epoch_ref.studyEpochId

  def key(self):
    return self._position_key
  
  # def add_encounter(self, encounter):
  #   self.usdm_timepoint.scheduledInstanceEncounterId = encounter.usdm_encounter.encounterId

  def add_activity(self, activity):
    self.usdm_timepoint.activityIds.append(activity.usdm_activity.activityId)

  def _process_timepoint(self):
    rel_ref = 0
    timing_info = self.parent.read_cell(SoAColumnRows.TIMING_ROW, self.col_index)
    if not timing_info == "":
      self.window = self.parent.read_cell(SoAColumnRows.VISIT_WINDOW_ROW, self.col_index)
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
    instance = None
    if self.timing_type in ["anchor", "next", "previous", "cycle start"]:
      timing = self._to_timing()
      instance = ScheduledActivityInstance(
        scheduledInstanceId=id_manager.build_id(ScheduledActivityInstance),
        scheduledInstanceType='ACTIVITY',
        scheduleTimelineExitId="",
        scheduledInstanceEncounterId="",
        scheduledInstanceTimings=[timing],
        scheduledInstanceTimelineId="",
        defaultConditionId="",
        epochId="",
        activityIds=[]
      )
      timing.relativeFromScheduledInstanceId = instance.scheduledInstanceId
    elif self.timing_type == "condition":
      instance = ScheduledDecisionInstance(
        scheduledInstanceId=id_manager.build_id(ScheduledActivityInstance),
        scheduledInstanceType='DECISION',
        scheduleTimelineExitId="",
        scheduledInstanceEncounterId="",
        scheduledInstanceTimings=[],
        scheduledInstanceTimelineId="",
        defaultConditionId="",
        conditionAssignments=[]
      )
    else:
      print("TYPE:", self.timing_type)
    return instance

  def _to_timing(self):
    type_code = {
      "ANCHOR": CDISCCT().code('C99901x3', 'Fixed Reference'),
      "PREVIOUS": CDISCCT().code('C99901x1', 'After'),
      "NEXT": CDISCCT().code('C99901x2', 'Before'),
      "CYCLE START": CDISCCT().code('C99901x3', 'Fixed Reference'),
    }
    return Timing(
      timingId=id_manager.build_id(Timing),
      timingType=type_code[self.timing_type.upper()],
      timingValue=self.timing_value,
      timingRelativeToFrom=CDISCCT().code('C99900x1', 'Start to Start'),
      timingWindow=self.window,
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
    column = self.parent.sheet.iloc[:, self.col_index]
    row = 0
    for cell in column:
      if row >= SoAColumnRows.FIRST_ACTIVITY_ROW:
        activity = self.parent.read_cell(row, SoAColumnRows.CHILD_ACTIVITY_COL)
        if str(cell).upper() == "X":
          self.activity_map[activity] = True
      row += 1

