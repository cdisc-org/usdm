from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_sheet.timepoint_type import TimepointType
from usdm_excel.study_soa_sheet.window_type import WindowType
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.cdisc_ct import CDISCCT
from usdm_model.timing import Timing
from usdm_model.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
from usdm_model.encounter import Encounter
from usdm_model.study_epoch import StudyEpoch

class Timepoint():
  
  def __init__(self, parent, activity_names, col_index, type="", value="", cycle=None, additional=False):
    epoch_ref = None
    self.parent = parent
    self.col_index = col_index
    if col_index == None:
      self._position_key = None
    else:
      self._position_key = col_index - SoAColumnRows.FIRST_VISIT_COL
    self.encounter_xref = ""
    self.has_activities = not additional
    self.has_encounter = False
    if not additional:
      self.encounter_xref, encounter_is_null = self.parent.read_cell_empty_legacy(SoAColumnRows.VISIT_LABEL_ROW, col_index)
      if not self.encounter_xref == "":
        self.has_encounter = True
      self.epoch = self.parent.read_cell_with_previous(SoAColumnRows.EPOCH_ROW, col_index, SoAColumnRows.FIRST_VISIT_COL)
      epoch_ref = cross_references.get(StudyEpoch, self.epoch)
    self.activities = []
    self.activity_map = {}
    self.__timepoint_type = None
    self.reference = None
    self.timing_value = ""
    self.__window = None
    self.cycle = cycle
    if not additional:
      self._process_timepoint()
      self._add_activities(activity_names)
    else:
      self._synthetic_timepoint(type, value, cycle)
    self.usdm_timepoint = self._as_usdm()
    if self.has_encounter:
      encounter = cross_references.get(Encounter, self.encounter_xref)
      self.usdm_timepoint.scheduledActivityInstanceEncounterId = encounter.id
    if epoch_ref is not None:
      self.usdm_timepoint.epochId = epoch_ref.id

  def key(self):
    return self._position_key
  
  def add_activity(self, activity):
    self.usdm_timepoint.activityIds.append(activity.usdm_activity.id)

  def _process_timepoint(self):
    self.__timepoint_type = TimepointType(self.parent, SoAColumnRows.TIMING_ROW, self.col_index)
    self.reference = self.col_index - SoAColumnRows.FIRST_VISIT_COL + self.__timepoint_type.relative_ref
    self.__window = WindowType(self.parent, SoAColumnRows.VISIT_WINDOW_ROW, self.col_index)

  def _synthetic_timepoint(self, type, value, cycle):
    self.__timepoint_type = TimepointType(None, 0, 0)
    self.__timepoint_type.set_type(type, value, cycle)
    self.timing_value = value
    #self.reference = self.col_index - SoAColumnRows.FIRST_VISIT_COL + self.__timepoint_type.relative_ref
    self.__window = WindowType(None, 0, 0)

  def _as_usdm(self):
    instance = None
    if self.__timepoint_type.timing_type in ["anchor", "next", "previous", "cycle start"]:
      timing = self._to_timing()
      instance = ScheduledActivityInstance(
        id=id_manager.build_id(ScheduledActivityInstance),
        instanceType='ACTIVITY',
        scheduleTimelineExitId=None,
        scheduledInstanceEncounterId=None,
        scheduledInstanceTimings=[timing],
        scheduledInstanceTimelineId=None,
        defaultConditionId=None,
        epochId=None,
        activityIds=[]
      )
      cross_references.add(instance.id, instance)
      timing.relativeFromScheduledInstanceId = instance.id
    elif self.__timepoint_type.timing_type == "condition":
      instance = ScheduledDecisionInstance(
        id=id_manager.build_id(ScheduledActivityInstance),
        instanceType='DECISION',
        scheduleTimelineExitId=None,
        scheduledInstanceEncounterId=None,
        scheduledInstanceTimings=[],
        scheduledInstanceTimelineId=None,
        defaultConditionId=None,
        conditionAssignments=[]
      )
      cross_references.add(instance.id, instance)
    else:
      self.parent._general_warning(f"Unrecognized ScheduledInstance type: '{self.__timepoint_type.timing_type}'")
    return instance

  def _to_timing(self):
    type_code = {
      "ANCHOR": CDISCCT().code('C99901x3', 'Fixed Reference'),
      "PREVIOUS": CDISCCT().code('C99901x1', 'After'),
      "NEXT": CDISCCT().code('C99901x2', 'Before'),
      "CYCLE START": CDISCCT().code('C99901x3', 'Fixed Reference'),
    }
    return Timing(
      id=id_manager.build_id(Timing),
      type=type_code[self.__timepoint_type.timing_type.upper()],
      timingValue=self.__timepoint_type.value,
      name=f"TIMING_{self.col_index}", # TODO: Temporary fix, need something better
      description=self.__timepoint_type.description,
      label="",
      timingRelativeToFrom=CDISCCT().code('C99900x1', 'Start to Start'),
      timingWindow=self.__window.description,
      timingWindowLower=self.__window.lower,
      timingWindowUpper=self.__window.upper,
      relativeFromScheduledInstanceId='',
      relativeToScheduledInstanceId=''
    )

  def get_relative_ref(self, part):
    if len(part) > 1:
      return int(part[1:])
    else:
      return 1

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

