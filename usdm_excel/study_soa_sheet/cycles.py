from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import IdManager
import pandas as pd

class Cycles:
  
  def __init__(self, sheet, id_manager: IdManager):
    self.sheet = sheet
    self.id_manager = id_manager
    
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

  def previous_index(index):
    if index == 0:
      return 0
    else:
      return index - 1

  def build_cycle_record(self, index, col_index, cycle):
    cycle_start_index = index
    cycle_start, is_null = self.get_cycle_cell(SoAColumnRows.CYCLE_START_ROW, col_index)
    cycle_period, is_null = self.get_cycle_cell(SoAColumnRows.CYCLE_PERIOD_ROW, col_index)
    cycle_end_rule, is_null = self.get_cycle_cell(SoAColumnRows.CYCLE_END_RULE_ROW, col_index)
    return { 
      'start_index': cycle_start_index, 
      'cycle': cycle, 
      'start': cycle_start, 
      'period': cycle_period, 
      'end_rule': cycle_end_rule 
    }

  def extract(self):
    cycles = []
    timepoint_index = -1
    cycle_start_index = None
    in_cycle = False
    prev_cycle = None
    for col_index in range(self.sheet.shape[1]):
      if col_index >= SoAColumnRows.FIRST_VISIT_COL:
        timepoint_index += 1
        cycle, cycle_is_null = self.get_cycle_cell(SoAColumnRows.CYCLE_ROW, col_index)
        if cycle_is_null:
          if in_cycle:
            cycle_record['end_index'] = self.previous_index(timepoint_index)
            cycles.append(cycle_record)
            in_cycle = False
          else:
            pass # Do nothing
        else:
          cycle = str(cycle)
          if not in_cycle:
            in_cycle = True
            cycle_record = self.build_cycle_record(timepoint_index, col_index, cycle)
          elif prev_cycle == cycle:
            pass # Do nothing
          else:
            cycle_record['end_index'] = self.previous_index(timepoint_index)
            cycles.append(cycle_record)
            cycle_record = self.build_cycle_record(timepoint_index, col_index, cycle)
        prev_cycle = cycle
    return cycles