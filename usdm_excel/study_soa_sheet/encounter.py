from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import id_manager
from usdm.encounter import Encounter as USDMEncounter
from usdm_excel.cross_ref import cross_references

class Encounter(BaseSheet):
  
  def __init__(self, sheet, col_index):
    super().__init__(sheet)
    self._position_key = col_index - SoAColumnRows.FIRST_VISIT_COL
    self.xref = self.clean_cell_unnamed(SoAColumnRows.VISIT_LABEL_ROW, col_index)
    self.epoch, is_null = self.clean_cell_unnamed_with_previous(SoAColumnRows.EPOCH_ROW, col_index, SoAColumnRows.FIRST_VISIT_COL)
    self.usdm_encounter = cross_references.get(self.xref)

  def key(self):
    return self._position_key