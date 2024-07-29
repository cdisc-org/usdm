from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_v2_sheet.soa_column_rows import SoAColumnRows
from usdm_model.activity import Activity
from usdm_model.biomedical_concept_surrogate import BiomedicalConceptSurrogate
from usdm_model.procedure import Procedure
from usdm_model.schedule_timeline import ScheduleTimeline

class SoAActivity():
  
  def __init__(self, parent: BaseSheet, row_index: int):
    self.parent = parent
    self.row_index = row_index
    self.usdm_biomedical_concept_surrogates = []
    self.usdm_biomedical_concepts = []
    self.parent_activity = parent.read_cell(row_index, SoAColumnRows.ACTIVITY_COL)
    self.name = parent.read_cell(row_index, SoAColumnRows.CHILD_ACTIVITY_COL)
    self._bcs, self._prs, self._tls = self._get_observation_cell(row_index, SoAColumnRows.BC_COL)
    self.parent._debug(row_index, SoAColumnRows.BC_COL, f"Activity {self.name} read. BC: {self._bcs}, PR: {self._prs}, TL: {self._tls}")
    self.usdm_activity = self._as_usdm()
    
  def _as_usdm(self) -> Activity:
    surrogate_bc_items = []
    full_bc_items = []
    for bc in self._bcs:
      if self.parent.globals.cdisc_bc_library.exists(bc):
        full_bc = self.parent.globals.cdisc_bc_library.usdm(bc)
        full_bc_items.append(full_bc.id)
        self.usdm_biomedical_concepts.append(full_bc)
        self.parent.globals.cross_references.add(full_bc.id, full_bc)
      else:
        params = {'name': bc, 'description': bc, 'label': bc, 'reference': 'None set'}
        item = self.parent.create_object(BiomedicalConceptSurrogate, params)
        if item:
          surrogate_bc_items.append(item.id)
          self.usdm_biomedical_concept_surrogates.append(item)
          self.parent.globals.cross_references.add(item.id, item)
    timeline = self._set_timeline()
    # if len(self._tls) > 0:
    #   timeline = self.parent.globals.cross_references.get(ScheduleTimeline, self._tls[0])
    #   if timeline:
    #     timelineId = timeline.id
    #   else:
    #     timelineId = None
    #     self.parent._general_error(f"Unable to find timeline with name '{self._tls[0]}'")
    procedures = self._set_procedures()
    # for procedure in self._prs:
    #   ref = self.parent.globals.cross_references.get(Procedure, procedure)
    #   if ref:
    #     procedures.append(ref)
    #   else:
    #     self.parent._warning(self.row_index, SoAColumnRows.BC_COL, f"Cross reference error for procedure {procedure}, not found")
    activity = self.parent.globals.cross_references.get(Activity, self.name)
    if activity is None:
      params = {'name': self.name, 'description': self.name, 
                'label': self.name, 'definedProcedures': procedures, 
                'biomedicalConceptIds': full_bc_items, 'bcCategoryIds': [], 
                'bcSurrogateIds': surrogate_bc_items, 'timelineId': timeline.id if timeline else None}
      activity = self.parent.create_object(Activity, params)
      if activity:
        self.parent.globals.cross_references.add(self.name, activity)     
        self.parent._warning(self.row_index, SoAColumnRows.BC_COL, f"No activity {self.name} found, so one has been created")
    else:
      activity.definedProcedures = procedures
      activity.biomedicalConceptIds = full_bc_items
      activity.bcSurrogateIds = surrogate_bc_items
      activity.timelineId = timeline.id if timeline else None
    return activity
  
  def _set_procedures(self):
    results = []
    for procedure in self._prs:
      ref = self.parent.globals.cross_references.get(Procedure, procedure)
      if ref:
        results.append(ref)
      else:
        self.parent._warning(self.row_index, SoAColumnRows.BC_COL, f"Cross reference error for procedure {procedure}, not found")
    return results
  
  def _set_timeline(self):
    result = None
    if self._tls:
      result = self.parent.globals.cross_references.get(ScheduleTimeline, self._tls[0])
      if not result:
        self.parent._general_error(f"Unable to find timeline with name '{self._tls[0]}'")
    return result

  def _get_observation_cell(self, row_index: int, col_index: int) -> tuple[list, list, list]:
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
