from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_v2_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.cdisc_ct import CDISCCT
from usdm_model.timing import Timing
from usdm_model.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
from usdm_model.encounter import Encounter
from usdm_model.study_epoch import StudyEpoch

class ScheduledInstance():
  
  def __init__(self, parent, activity_names, col_index):
    epoch_ref = None
    self.parent = parent
    self.encounter_xref = None
    self.epoch_name = self.parent.read_cell_with_previous(SoAColumnRows.EPOCH_ROW, col_index, SoAColumnRows.FIRST_VISIT_COL)
    self.encounter_name = self.read_cell(SoAColumnRows.ENCOUNTER_ROW, col_index)
    self.type = self.read_cell(SoAColumnRows.TYPE_ROW, col_index)
    self.default_name = self.read_cell(SoAColumnRows.DEFAULT_ROW, col_index)
    self.conditions = self.read_cell(SoAColumnRows.CONDITIONS_ROW, col_index)
    self.activities = []
    self.activity_map = {}
    self._add_activities(activity_names)
    self.usdm_timepoint = self._as_usdm()
    if self.encounter_name:
      encounter = cross_references.get(Encounter, self.encounter_name)
      self.encounter_id = encounter.id
    if self.epoch_name:
      epoch = cross_references.get(StudyEpoch, self.epoch)
      self.epoch_id = epoch.id

  def add_activity(self, activity):
    self.usdm_timepoint.activityIds.append(activity.usdm_activity.id)

  def _as_usdm(self):
    instance = None
    if self.type.upper() == "ACTIVITY":
      instance = ScheduledActivityInstance(
        id=id_manager.build_id(ScheduledActivityInstance),
        instanceType=self.type,
        scheduleTimelineExitId=None,
        scheduledInstanceEncounterId=self.encounter_id,
        scheduledInstanceTimings=[],
        scheduledInstanceTimelineId=None,
        defaultConditionId=None,
        epochId=self.epoch_id,
        activityIds=[]
      )
    elif self.type == "CONDITION":
      instance = ScheduledDecisionInstance(
        id=id_manager.build_id(ScheduledActivityInstance),
        instanceType=self.type,
        scheduleTimelineExitId=None,
        scheduledInstanceEncounterId=None,
        scheduledInstanceTimings=[],
        scheduledInstanceTimelineId=None,
        defaultConditionId=None,
        conditionAssignments=[]
      )
    else:
      self.parent.general_warning(f"Unrecognized ScheduledInstance type: '{self.__timepoint_type.timing_type}'")
    return instance

  def _add_activities(self, activity_names):
    for activity in activity_names:
      self.activity_map[activity] = False
    column = self.parent.sheet.iloc[:, self.col_index]
    row = 0
    for cell in column:
      if row >= SoAColumnRows.FIRST_ACTIVITY_ROW:
        activity = self.parent.read_cell(row, SoAColumnRows.CHILD_ACTIVITY_COL)
        if str(cell).upper() == "X":
          self.activity_map[activity] = True
      row += 1

