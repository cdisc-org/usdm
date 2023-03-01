from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import IdManager
from usdm.encounter import Encounter as USDMEncounter

class Encounter(BaseSheet):
  
  def __init__(self, sheet, id_manager: IdManager, col_index):
    super().__init__(sheet, id_manager)
    #self._col_index = col_index
    self._position_key = col_index - SoAColumnRows.FIRST_VISIT_COL
    self.name = self.clean_cell_unnamed(SoAColumnRows.VISIT_LABEL_ROW, col_index)
    self.epoch, is_null = self.clean_cell_unnamed_with_previous(SoAColumnRows.EPOCH_ROW, col_index, SoAColumnRows.FIRST_VISIT_COL)
    self.window = self.clean_cell_unnamed(SoAColumnRows.VISIT_WINDOW_ROW, col_index)
    self.usdm_encounter = self._as_usdm()

  def key(self):
    return self._position_key
  
  def _as_usdm(self):
    return USDMEncounter(
      encounterId=self.id_manager.build_id(Encounter),
      encounterName=self.name,
      encounterDescription=self.name,
      #encounterType: Union[Code, None] = None,
      #encounterEnvironmentalSetting: Union[Code, None] = None,
      #encounterContactModes: List[Code] = []
      encounterScheduledAtTimingId=None
    )