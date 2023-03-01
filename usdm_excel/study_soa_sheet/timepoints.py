from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_sheet.timepoint import Timepoint
from usdm_excel.id_manager import IdManager
import pandas as pd

class Timepoints(BaseSheet):
  
  def __init__(self, sheet, id_manager: IdManager):
    super().__init__(sheet, id_manager)
    self.sheet = sheet
    self.id_manager = id_manager
    self.items = []
    self.map = {}
    self.activity_names = []
    self._build_activities()
    self._build_timepoints()

  def item_at(self, key):
    return self.map[key]

  def _build_timepoints(self):    
    for col_index in range(self.sheet.shape[1]):
      if col_index >= SoAColumnRows.FIRST_VISIT_COL:
        record = Timepoint(self.sheet, self.id_manager, self.activity_names, col_index, True)
        self.items.append(record)
        self.map[record.key()] = record

  def _build_activities(self):    
    for row_index, col_def in self.sheet.iterrows():
      if row_index >= SoAColumnRows.FIRST_ACTIVITY_ROW:
        activity = self.clean_cell_unnamed(row_index, SoAColumnRows.CHILD_ACTIVITY_COL)
        if not activity == "":
          self.activity_names.append(activity)
