from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import IdManager
from usdm_excel.study_soa_sheet.encounter import Encounter

class Encounters:
  
  def __init__(self, sheet):
    self.sheet = sheet
    self.items = []
    self.map = {}
    for col_index in range(self.sheet.shape[1]):
      if col_index >= SoAColumnRows.FIRST_VISIT_COL:
        record = Encounter(self.sheet, col_index)
        self.items.append(record)
        self.map[record.position_key] = record

  def item_at(self, key):
    return self.map[key]
