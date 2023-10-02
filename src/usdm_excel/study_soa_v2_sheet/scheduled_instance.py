from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_v2_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_v2_sheet.conditons import Conditons
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_model.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
from usdm_model.encounter import Encounter
from usdm_model.study_epoch import StudyEpoch
from usdm_model.activity import Activity
import traceback

class ScheduledInstance():
  
  def __init__(self, parent, col_index):
    self.parent = parent
    self.item = None
    self.col_index = col_index
    epoch_id = None
    encounter_id = None
    name = self.parent.read_cell(SoAColumnRows.NAME_ROW, col_index)
    self.name = name
    description = self.parent.read_cell(SoAColumnRows.DESCRIPTION_ROW, col_index)
    label = self.parent.read_cell(SoAColumnRows.LABEL_ROW, col_index)
    epoch_name = self.parent.read_cell(SoAColumnRows.EPOCH_ROW, col_index)
    encounter_name = self.parent.read_cell(SoAColumnRows.ENCOUNTER_ROW, col_index)
    type = self.parent.read_cell(SoAColumnRows.TYPE_ROW, col_index)
    self.default_name = self.parent.read_cell(SoAColumnRows.DEFAULT_ROW, col_index)
    self.conditions = Conditons(self.parent.read_cell(SoAColumnRows.CONDITIONS_ROW, col_index))
    if encounter_name:
      encounter = cross_references.get(Encounter, encounter_name)
      if encounter:
        encounter_id = encounter.id
      else:
        self.parent._general_warning(f"Failed to find encounter with name '{encounter_name}'")
    if epoch_name:
      epoch = cross_references.get(StudyEpoch, epoch_name)
      if epoch:
        epoch_id = epoch.id
      else:
        self.parent._general_warning(f"Failed to find epoch with name '{epoch_name}'")
    try:
      if type.upper() == "ACTIVITY":
        self.item = ScheduledActivityInstance(
          id=id_manager.build_id(ScheduledActivityInstance),
#          name=name,
#          description=description,
#          label=label,
          instanceType='ACTIVITY',
          scheduleTimelineExitId=None,
          scheduledInstanceEncounterId=encounter_id,
          scheduledInstanceTimings=[],
          scheduledInstanceTimelineId=None,
          defaultConditionId=None,
          epochId=epoch_id,
          activityIds=self._add_activities()
        )
        cross_references.add(self.item.id, self.item)
      elif type.upper() == "DECISION":
        self.item = ScheduledDecisionInstance(
          id=id_manager.build_id(ScheduledDecisionInstance),
          instanceType='DECISION',
          scheduleTimelineExitId=None,
          scheduledInstanceEncounterId=None,
          scheduledInstanceTimings=[],
          scheduledInstanceTimelineId=None,
          defaultConditionId=None,
          conditionAssignments=[]
        )
        cross_references.add(self.item.id, self.item)
      else:
        self.parent._general_warning(f"Unrecognized ScheduledInstance type: '{type}'")
    except Exception as e:
      self.parent._general_error(f"Exception [{e}] raised reading sheet")
      self.parent._traceback(f"{traceback.format_exc()}")

  def _add_activities(self):
    activities = []
    row = 0
    column = self.parent.sheet.iloc[:, self.col_index]
    for cell in column:
      if row >= SoAColumnRows.FIRST_ACTIVITY_ROW:
        activity_name = self.parent.read_cell(row, SoAColumnRows.CHILD_ACTIVITY_COL)
        if str(cell).upper() == "X":
          activity = cross_references.get(Activity, activity_name)
          activities.append(activity.id)
      row += 1
    return activities

