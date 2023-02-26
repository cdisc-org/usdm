from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import IdManager
import pandas as pd

class Activity:
  
  def __init__(self, sheet, row_index):
    self.sheet = sheet
    self.row_index = row_index
    self.name = []
    self.bcs = []
    self.profiles = []
    self.name, activity_is_null = self.get_activity_cell(row_index, SoAColumnRows.CHILD_ACTIVITY_COL)
    self.bcs, self.profiles, obs_is_null = self.get_observation_cell(row_index, self.BC_COL)

  def get_observation_cell(self, row_index, col_index):
    bcs = []
    prs = []
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return [], [], True
    else:
      value = self.sheet.iloc[row_index, col_index]
      outer_parts = value.split(',')
      for outer_part in outer_parts:
        parts = outer_part.split(':')
        if parts[0].lower() == "bc":
          bcs.append(parts[1])
        elif parts[0].lower() == "pr":
          prs.append(parts[1])
        else:
          pass
      return bcs, prs, False

  def get_activity_cell(self, row_index, col_index):
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return "", True
    else:
      value = self.sheet.iloc[row_index, col_index]
      if value == '-':
        return "", True
      else:
        return self.sheet.iloc[row_index, col_index], False
