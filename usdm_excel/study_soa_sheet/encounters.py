from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import IdManager
from usdm_excel.study_soa_sheet.encounter import Encounter

class Encounters(BaseSheet):
  
  def __init__(self, sheet, id_manager: IdManager):
    super().__init__(sheet, id_manager)
    self.items = []
    self._map = {}
    self._epoch_map = {}
    for col_index in range(self.sheet.shape[1]):
      if col_index >= SoAColumnRows.FIRST_VISIT_COL:
        encounter = Encounter(self.sheet, self.id_manager, col_index)
        self.items.append(encounter)
        self._map[encounter.key()] = encounter
        if encounter.epoch not in self._epoch_map:
          self._epoch_map[encounter.epoch] = []
        self._epoch_map[encounter.epoch].append(encounter.usdm_encounter.encounterId)

  def item_at(self, key):
    return self._map[key]

  def epoch_encounter_map(self, epoch):
    return self._epoch_map[epoch]