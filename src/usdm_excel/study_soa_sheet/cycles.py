from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_sheet.cycle import Cycle
from usdm_excel.id_manager import id_manager
import pandas as pd

class Cycles():
  
  def __init__(self, parent):
    self.parent = parent
    self.items = []
    timepoint_index = -1
    in_cycle = False
    prev_cycle = None
    for col_index in range(self.parent.sheet.shape[1]):
      if col_index >= SoAColumnRows.FIRST_VISIT_COL:
        timepoint_index += 1
        #cycle, cycle_is_null = self._get_cycle_cell(SoAColumnRows.CYCLE_ROW, col_index)
        cycle, cycle_is_null = self.parent.read_cell_empty_legacy(SoAColumnRows.CYCLE_ROW, col_index)
        if cycle_is_null:
          if in_cycle:
            cycle_record.add_end(self.previous_index(timepoint_index))
            self.items.append(cycle_record)
            in_cycle = False
          else:
            pass # Do nothing
        else:
          cycle = str(cycle)
          if not in_cycle:
            in_cycle = True
            cycle_record = Cycle(self.parent, col_index, cycle, timepoint_index)
          elif prev_cycle == cycle:
            pass # Do nothing
          else:
            cycle_record.add_end(self.previous_index(timepoint_index))
            self.items.append(cycle_record)
            cycle_record = Cycle(self.parent, col_index, cycle, timepoint_index)
        prev_cycle = cycle
      
  # def _get_cycle_cell(self, row_index, col_index):
  #   if self.parent.cell_empty(row_index, col_index):
  #     return "", True
  #   else:
  #     value = self.parent.read_cell_empty(row_index, col_index, '-')
  #     if value == "":
  #       return "", True
  #     else:
  #       return value, False

  def previous_index(self, index):
    if index == 0:
      return 0
    else:
      return index - 1

