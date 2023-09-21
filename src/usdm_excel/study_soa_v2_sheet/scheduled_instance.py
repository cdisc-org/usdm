from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_v2_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.cdisc_ct import CDISCCT
from usdm_model.timing import Timing
from usdm_model.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
from usdm_model.encounter import Encounter
from usdm_model.study_epoch import StudyEpoch
import traceback

class ScheduledInstance():
  
  def __init__(self, parent, activity_names, col_index):
    self.parent = parent
    epoch_name = self.parent.read_cell_with_previous(SoAColumnRows.EPOCH_ROW, col_index, SoAColumnRows.FIRST_VISIT_COL)
    encounter_name = self.read_cell(SoAColumnRows.ENCOUNTER_ROW, col_index)
    type = self.read_cell(SoAColumnRows.TYPE_ROW, col_index)
    default_name = self.read_cell(SoAColumnRows.DEFAULT_ROW, col_index)
    conditions = self.read_cell(SoAColumnRows.CONDITIONS_ROW, col_index)
    activities = []
    activity_map = {}
    self._add_activities(activity_names)
    if encounter_name:
      encounter = cross_references.get(Encounter, encounter_name)
    if epoch_name:
      epoch = cross_references.get(StudyEpoch, epoch_name)
    try:
      instance = None
      if type.upper() == "ACTIVITY":
        instance = ScheduledActivityInstance(
          id=id_manager.build_id(ScheduledActivityInstance),
          instanceType=self.type,
          scheduleTimelineExitId=None,
          scheduledInstanceEncounterId=encounter.id,
          scheduledInstanceTimings=[],
          scheduledInstanceTimelineId=None,
          defaultConditionId=None,
          epochId=epoch.id,
          activityIds=[]
        )
      elif type.upper() == "CONDITION":
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
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet")
      self._traceback(f"{traceback.format_exc()}")

  # def add_activity(self, activity):
  #   self.usdm_timepoint.activityIds.append(activity.usdm_activity.id)

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

