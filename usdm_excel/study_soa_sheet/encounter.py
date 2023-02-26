from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import IdManager
import pandas as pd

class Encounter:
  
  def __init__(self, sheet, col_index):
    self.sheet = sheet
    self.col_index = col_index
    self.label, label_is_null = self.get_encounter_cell(SoAColumnRows.VISIT_LABEL_ROW, self.col_index)
    self.window, window_is_null = self.get_encounter_cell(SoAColumnRows.VISIT_WINDOW_ROW, self.col_index)
    
  def get_encounter_cell(self, row_index, col_index):
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return "", True
    else:
      return self.sheet.iloc[row_index, col_index], False