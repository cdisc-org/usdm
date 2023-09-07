from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_model.activity import Activity as USDMActivity
from usdm_model.biomedical_concept_surrogate import BiomedicalConceptSurrogate
from usdm_excel.cdisc_biomedical_concept import cdisc_bc_library
from usdm_model.procedure import Procedure
from usdm_model.schedule_timeline import ScheduleTimeline

class Activity():
  
  def __init__(self, parent, row_index):
    self.parent = parent
    self.row_index = row_index
    self.usdm_biomedical_concept_surrogates = []
    self.usdm_biomedical_concepts = []
    self.name = parent.read_cell(row_index, SoAColumnRows.CHILD_ACTIVITY_COL)
    self._bcs, self._prs, self._tls = self._get_observation_cell(row_index, SoAColumnRows.BC_COL)
    self.parent._debug(row_index, SoAColumnRows.BC_COL, f"Activity {self.name} read. BC: {self._bcs}, PR: {self._prs}, TL: {self._tls}")
    self.usdm_activity = self._as_usdm()
    
  def _as_usdm(self):
    surrogate_bc_items = []
    full_bc_items = []
    procedures = []
    for bc in self._bcs:
      if cdisc_bc_library.exists(bc):
        full_bc = cdisc_bc_library.usdm(bc)
        full_bc_items.append(full_bc.id)
        self.usdm_biomedical_concepts.append(full_bc)
      else:
        surrogate = self._to_bc_surrogates(bc)
        surrogate_bc_items.append(surrogate.id)
        self.usdm_biomedical_concept_surrogates.append(surrogate)
    timelineId = ""
    if len(self._tls) > 0:
      timeline = cross_references.get(ScheduleTimeline, self._tls[0])
      timelineId = timeline.id
    for procedure in self._prs:
      ref = cross_references.get(Procedure, procedure)
      if ref is not None:
        procedures.append(ref)
      else:
        self.parent._warning(self.row_index, SoAColumnRows.BC_COL, f"Cross reference error for procedure {procedure}, not found")
    activity = cross_references.get(Activity, self.name)
    if activity is None:
      activity = USDMActivity(
        id=id_manager.build_id(Activity),
        name=self.name,
        description=self.name,
        definedProcedures=procedures,
        activityIsConditional=False,
        activityIsConditionalReason="",
        biomedicalConceptIds=full_bc_items,
        bcCategoryIds=[],
        bcSurrogateIds=surrogate_bc_items,
        activityTimelineId=timelineId
      )
    else:
      activity.definedProcedures = procedures
      activity.biomedicalConceptIds = full_bc_items
      activity.bcSurrogateIds = surrogate_bc_items
      activity.activityTimelineId = timelineId
    return activity
  
  def _to_bc_surrogates(self, name):
    return BiomedicalConceptSurrogate(
      id=id_manager.build_id(BiomedicalConceptSurrogate),
      name=name,
      description=name,
      label=name,
      bcSurrogateReference='None set'
    )
  
  def _get_observation_cell(self, row_index, col_index):
    bcs = []
    prs = []
    tls = []
    if not self.parent.cell_empty(row_index, col_index):
      value = self.parent.read_cell(row_index, col_index)
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
    return bcs, prs, tls
