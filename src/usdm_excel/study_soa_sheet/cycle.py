from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import id_manager
import pandas as pd

class Cycle():
  
  def __init__(self, parent, col_index, cycle, timepoint_index):
    self.parent = parent
    self.col_index = col_index
    self.position_key = col_index - SoAColumnRows.FIRST_VISIT_COL
    self.cycle = cycle
    self.start_timepoint_index = timepoint_index
    self.end_timepoint_index = timepoint_index
    self.start = self.get_cycle_cell(SoAColumnRows.CYCLE_START_ROW, col_index)
    self.period = self.get_cycle_cell(SoAColumnRows.CYCLE_PERIOD_ROW, col_index)
    self.end_rule = self.get_cycle_cell(SoAColumnRows.CYCLE_END_RULE_ROW, col_index)

  def add_end(self, index):
    self.end_timepoint_index = index

  def get_cycle_cell(self, row_index, col_index):
    return self.parent.read_cell_empty(row_index, col_index, '-')

