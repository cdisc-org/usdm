from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import IdManager
import pandas as pd

class Cycle(BaseSheet):
  
  def __init__(self, sheet, id_manager: IdManager, col_index, cycle, timepoint_index):
    super().__init__(sheet, id_manager)
    self.col_index = col_index
    self.position_key = col_index - SoAColumnRows.FIRST_VISIT_COL
    self.cycle = cycle
    self.start_timepoint_index = timepoint_index
    self.end_timepoint_index = timepoint_index
    self.start, is_null = self.get_cycle_cell(SoAColumnRows.CYCLE_START_ROW, col_index)
    self.period, is_null = self.get_cycle_cell(SoAColumnRows.CYCLE_PERIOD_ROW, col_index)
    self.end_rule, is_null = self.get_cycle_cell(SoAColumnRows.CYCLE_END_RULE_ROW, col_index)

  def add_end(self, index):
    self.end_timepoint_index = index

  def get_cycle_cell(self, row_index, col_index):
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return "", True
    else:
      value = str(self.sheet.iloc[row_index, col_index])
      if value.upper() == "-":
        return "", True
      else:
        return value, False

