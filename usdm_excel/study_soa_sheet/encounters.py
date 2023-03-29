from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
import pandas as pd

class Encounters(BaseSheet):
  
  def __init__(self, sheet):
    super().__init__(sheet)
    self._epoch_map = {}
    for col_index in range(self.sheet.shape[1]):
      if col_index >= SoAColumnRows.FIRST_VISIT_COL:
        self.xref, is_null = self._get_xref_cell(SoAColumnRows.VISIT_LABEL_ROW, col_index)
        self.epoch, is_null = self.clean_cell_unnamed_with_previous(SoAColumnRows.EPOCH_ROW, col_index, SoAColumnRows.FIRST_VISIT_COL)
        if not self.xref == "":
          #print("XREF:", self.xref)
          encounter = cross_references.get(self.xref)
          if self.epoch not in self._epoch_map:
            self._epoch_map[self.epoch] = []
          self._epoch_map[self.epoch].append(encounter.encounterId)

  def epoch_encounter_map(self, epoch):
    return self._epoch_map[epoch]
  
  def _get_xref_cell(self, row_index, col_index):
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return "", True
    else:
      value = str(self.sheet.iloc[row_index, col_index])
      if value.upper() == "-":
        return "", True
      else:
        return value, False