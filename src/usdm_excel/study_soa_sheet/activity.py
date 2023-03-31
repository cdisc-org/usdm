from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_model.activity import Activity as USDMActivity
from usdm_model.biomedical_concept_surrogate import BiomedicalConceptSurrogate
from usdm_excel.cdisc_biomedical_concept import CDISCBiomedicalConcepts
import pandas as pd

class Activity():
  
  def __init__(self, parent, row_index):
    #super().__init__(sheet)
    #self._row_index = row_index
    self.parent = parent
    self.usdm_biomedical_concept_surrogates = []
    self.usdm_biomedical_concepts = []
    self.name, activity_is_null = parent.clean_cell_unnamed_new(row_index, SoAColumnRows.CHILD_ACTIVITY_COL)
    self._bcs, self._prs, self._tls, obs_is_null = self._get_observation_cell(row_index, SoAColumnRows.BC_COL)
    self.usdm_activity = self._as_usdm()
    
  def _as_usdm(self):
    surrogate_bc_items = []
    full_bc_items = []
    procedures = []
    cdisc_bcs = CDISCBiomedicalConcepts()
    for bc in self._bcs:
      if cdisc_bcs.exists(bc):
        full_bc = cdisc_bcs.usdm(bc)
        full_bc_items.append(full_bc.biomedicalConceptId)
        self.usdm_biomedical_concepts.append(full_bc)
      else:
        surrogate = self._to_bc_surrogates(bc)
        surrogate_bc_items.append(surrogate.bcSurrogateId)
        self.usdm_biomedical_concept_surrogates.append(surrogate)
    timelineId = ""
    if len(self._tls) > 0:
      timelineId = cross_references.get(self._tls[0])
    for procedure in self._prs:
      procedures.append(cross_references.get(procedure))
    return USDMActivity(
      activityId=id_manager.build_id(Activity),
      activityName=self.name,
      activityDescription=self.name,
      definedProcedures=procedures,
      activityIsConditional=False,
      activityIsConditionalReason="",
      biomedicalConceptIds=full_bc_items,
      bcCategoryIds=[],
      bcSurrogateIds=surrogate_bc_items,
      activityTimelineId=timelineId
    )
  
  def _to_bc_surrogates(self, name):
    return BiomedicalConceptSurrogate(
      bcSurrogateId=id_manager.build_id(BiomedicalConceptSurrogate),
      bcSurrogateName=name,
      bcSurrogateDescription=name,
      bcSurrogateReference=''
    )
  
  def _get_observation_cell(self, row_index, col_index):
    bcs = []
    prs = []
    tls = []
    is_null = pd.isnull(self.parent.sheet.iloc[row_index, col_index])
    if is_null:
      return [], [], [], True
    else:
      value = self.parent.sheet.iloc[row_index, col_index]
      outer_parts = value.split(',')
      for outer_part in outer_parts:
        parts = outer_part.split(':')
        if parts[0].strip().upper() == "BC":
          bcs.append(parts[1].strip())
        elif parts[0].strip().upper() == "PR":
          prs.append(parts[1].strip())
        elif parts[0].strip().upper() == "TL":
          tls.append(parts[1].strip())
        else:
          pass
      return bcs, prs, tls, False
