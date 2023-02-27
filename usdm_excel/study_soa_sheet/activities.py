from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import IdManager
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_sheet.activity import Activity
import pandas as pd

class Activities(BaseSheet):
  
  def __init__(self, sheet, id_manager: IdManager):
    super().__init__(sheet, id_manager)
    self.items = []
    self.map = {}
    for row_index, col_def in self.sheet.iterrows():
      if row_index >= SoAColumnRows.FIRST_ACTIVITY_ROW:
        activity = Activity(self.sheet, self.id_manager, row_index)
        self.items.append(activity)
        self.map[activity.name] = activity

  def item_by_name(self, name):
    return self.map[name]