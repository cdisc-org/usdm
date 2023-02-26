from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_sheet.timepoint import Timepoint
from usdm_excel.id_manager import IdManager
import pandas as pd

class Timepoints:
  
  def __init__(self, sheet, id_manager: IdManager):
    self.sheet = sheet
    self.id_manager = id_manager
    self.items = []
    for col_index in range(self.sheet.shape[1]):
      if col_index >= SoAColumnRows.FIRST_VISIT_COL:
        record = Timepoint(self.sheet, col_index)
        self.items.append(record)

