from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import IdManager
import pandas as pd

class Timepoint:
  
  def __init__(self, sheet, col_index):
    self.sheet = sheet
    self.col_index = col_index
    self.timing_type = ""
    rel_ref = 0
    self.timing_value = ""
    timing_info, timing_info_is_null = self.get_timing_cell(SoAColumnRows.TIMING_ROW, self.col_index)
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
    self.cycle = None

  def get_timing_cell(self, row_index, col_index):
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return "", True
    else:
      return self.sheet.iloc[row_index, col_index], False

  def get_relative_ref(self, part):
    if len(part) > 1:
      return int(part[1:])
    else:
      return 1

  def activities(self, index):
    self.activities = {}
    for activity in self.activities:
      self.activities[activity] = False
    column = self.sheet.iloc[:, index]
    row = 0
    for col in column:
      if row >= self.FIRST_ACTIVITY_ROW:
        activity, activity_is_null = self.get_activity_cell(row, SoAColumnRows.ACTIVITY_COL)
        if col.upper() == "X":
          self.activities[activity] = True
    row += 1

  def get_activity_cell(self, row_index, col_index):
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return "", True
    else:
      return self.sheet.iloc[row_index, col_index], False
