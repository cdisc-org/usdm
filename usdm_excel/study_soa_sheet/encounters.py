from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import IdManager
from usdm_excel.study_soa_sheet.encounter import Encounter

class Encounters(BaseSheet):
  
  def __init__(self, sheet, id_manager: IdManager):
    super().__init__(sheet, id_manager)
    self.items = []
    self.map = {}
    for col_index in range(self.sheet.shape[1]):
      if col_index >= SoAColumnRows.FIRST_VISIT_COL:
        record = Encounter(self.sheet, self.id_manager, col_index)
        self.items.append(record)
        self.map[record.position_key] = record

  def item_at(self, key):
    return self.map[key]
