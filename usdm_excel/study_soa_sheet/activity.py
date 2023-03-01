from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import IdManager
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm.activity import Activity as USDMActivity
from usdm.biomedical_concept_surrogate import BiomedicalConceptSurrogate
import pandas as pd

class Activity(BaseSheet):
  
  def __init__(self, sheet, id_manager: IdManager, row_index):
    super().__init__(sheet, id_manager)
    self.row_index = row_index
    self.name = []
    self.biomedical_concept_surrogates = []
    self.bcs = []
    self.prs = []
    self.name, activity_is_null = self.clean_cell_unnamed_new(row_index, SoAColumnRows.CHILD_ACTIVITY_COL)
    self.bcs, self.prs, obs_is_null = self._get_observation_cell(row_index, SoAColumnRows.BC_COL)

  def as_usdm(self):
    bc_items = []
    for bc in self.bcs:
      surrogate = self._to_bc_surrogates(bc)
      bc_items.append(surrogate.bcSurrogateId)
      self.biomedical_concept_surrogates.append(surrogate)

    return USDMActivity(
      activityId=self.id_manager.build_id(Activity),
      activityName="",
      activityDescription="",
      definedProcedures=[],
      activityIsConditional=False,
      activityIsConditionalReason="",
      biomedicalConcepts=[],
      bcCategories=[],
      bcSurrogates=bc_items,
      activityTimelineId=""
    )
  
  def _to_bc_surrogates(self, name):
    return BiomedicalConceptSurrogate(
      bcSurrogateId=self.id_manager.build_id(BiomedicalConceptSurrogate),
      bcSurrogateName=name,
      bcSurrogateDescription=name,
      bcSurrogateReference=''
    )
  
  def _get_observation_cell(self, row_index, col_index):
    bcs = []
    prs = []
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return [], [], True
    else:
      value = self.sheet.iloc[row_index, col_index]
      outer_parts = value.split(',')
      for outer_part in outer_parts:
        parts = outer_part.split(':')
        if parts[0].lower() == "bc":
          bcs.append(parts[1])
        elif parts[0].lower() == "pr":
          prs.append(parts[1])
        else:
          pass
      return bcs, prs, False
