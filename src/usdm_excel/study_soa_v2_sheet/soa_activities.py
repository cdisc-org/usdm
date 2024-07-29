#from usdm_excel.id_manager import id_manager
from usdm_excel.study_soa_v2_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_v2_sheet.soa_activity import SoAActivity
import pandas as pd

class SoAActivities():
  
  def __init__(self, parent):
    self.parent = parent
    self.items = []
    self.map = {}
    for row_index, col_def in parent.sheet.iterrows():
      if row_index >= SoAColumnRows.FIRST_ACTIVITY_ROW:
        activity = SoAActivity(self.parent, row_index)
        self.items.append(activity)
