from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_sheet.timepoint import Timepoint
from usdm_excel.id_manager import id_manager
from usdm.scheduled_instance import ScheduledInstanceType
import pandas as pd

class Timepoints(BaseSheet):
  
  def __init__(self, sheet):
    super().__init__(sheet)
    self.sheet = sheet
    self.items = []
    self.map = {}
    self.activity_names = []
    self._build_activities()
    self._build_timepoints()
    self._set_to_timing_refs()

  def item_at(self, key):
    return self.map[key]

  def insert_at(self, insert_at_index, type, value, cycle, reference=None):
    timepoint = Timepoint(self.sheet, self.activity_names, None, type, value, cycle, additional=True)
    timepoint.reference = reference
    self.items.insert(insert_at_index, timepoint)
    return timepoint
  
  def set_condition_refs(self):
    for item in self.items:
      condition = item.usdm_timepoint
      if condition.scheduledInstanceType == ScheduledInstanceType.DECISION:
        condition_instance = self.items[item.reference].usdm_timepoint
        text = item.timing_value
        if text == "":
          text = "default, no condition set"
        condition.conditionAssignments.append([text, condition_instance.scheduledInstanceId])
    previous_item = None
    for item in self.items:
      if previous_item == None:
        previous_item = item        
        continue
      previous_condition = previous_item.usdm_timepoint
      if previous_condition.scheduledInstanceType == ScheduledInstanceType.DECISION:
        current_instance = item.usdm_timepoint
        previous_condition.conditionAssignments.append(["default", current_instance.scheduledInstanceId])        
      previous_item = item        


  def _build_timepoints(self):    
    for col_index in range(self.sheet.shape[1]):
      if col_index >= SoAColumnRows.FIRST_VISIT_COL:
        record = Timepoint(self.sheet, self.activity_names, col_index, True)
        self.items.append(record)
        self.map[record.key()] = record

  def _build_activities(self):    
    for row_index, col_def in self.sheet.iterrows():
      if row_index >= SoAColumnRows.FIRST_ACTIVITY_ROW:
        activity = self.clean_cell_unnamed(row_index, SoAColumnRows.CHILD_ACTIVITY_COL)
        if not activity == "":
          self.activity_names.append(activity)

  def _set_to_timing_refs(self):    
    for item in self.items:
      from_instance = item.usdm_timepoint
      from_timing = from_instance.scheduledInstanceTimings[0]
      from_timing_type = from_timing.timingType.code
      if from_timing_type == "ANCHOR":
        continue
      to_instance = self.items[item.reference].usdm_timepoint
      from_timing.relativeToScheduledInstanceId = to_instance.scheduledInstanceId