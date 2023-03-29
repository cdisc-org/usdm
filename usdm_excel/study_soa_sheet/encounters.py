from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.study_soa_sheet.encounter import Encounter

class Encounters(BaseSheet):
  
  def __init__(self, sheet):
    super().__init__(sheet)
    #self.items = []
    #self._map = {}
    self._epoch_map = {}
    #print("ENC1:")
    for col_index in range(self.sheet.shape[1]):
      if col_index >= SoAColumnRows.FIRST_VISIT_COL:
        self.xref = self.clean_cell_unnamed(SoAColumnRows.VISIT_LABEL_ROW, col_index)
        self.epoch, is_null = self.clean_cell_unnamed_with_previous(SoAColumnRows.EPOCH_ROW, col_index, SoAColumnRows.FIRST_VISIT_COL)
        if not self.xref == "":
          encounter = cross_references.get(self.xref)
          if self.epoch not in self._epoch_map:
            self._epoch_map[self.epoch] = []
          self._epoch_map[self.epoch].append(encounter.encounterId)

  # def item_at(self, key):
  #   if key in self._map:
  #     return self._map[key]
  #   return None

  def epoch_encounter_map(self, epoch):
    #print("ENC3:", epoch, self._epoch_map)
    return self._epoch_map[epoch]