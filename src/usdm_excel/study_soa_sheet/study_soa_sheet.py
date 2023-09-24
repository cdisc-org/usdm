from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.study_soa_sheet.cycles import Cycles
from usdm_excel.study_soa_sheet.timepoints import Timepoints
from usdm_excel.study_soa_sheet.timepoint import Timepoint
from usdm_excel.study_soa_sheet.activities import Activities
from usdm_model.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_model.schedule_timeline_exit import ScheduleTimelineExit

import traceback

class StudySoASheet(BaseSheet):

  NAME_ROW = 0
  DESCRIPTION_ROW = 1
  CONDITION_ROW = 2
  PARAMS_DATA_COL = 1

  def __init__(self, file_path, sheet_name, main=False, require={}):
    try:
      super().__init__(file_path=file_path, sheet_name=sheet_name, header=None, require=require)
      if self.success:
        self.name = ""
        self.description = ""
        self.condition = ""
        self.timeline = None
        self.main_timeline = main
        self.encounters = []
        self.activities = []
        self.timelines = []
        self.biomedical_concept_surrogates = []
        self.biomedical_concepts = []
        self._process_sheet()
        self._raw_cycles = Cycles(self)
        self._raw_timepoints = Timepoints(self)
        #self._raw_encounters = Encounters(self)
        self._raw_activities = Activities(self)

        self._link_instance_to_activities()
        self._insert_cycles_into_timeline()
        self._raw_timepoints.set_condition_refs()

        instances = []

        for item in self._raw_activities.items:
          activity = item.usdm_activity
          self.activities.append(activity)
          self.biomedical_concept_surrogates += item.usdm_biomedical_concept_surrogates
          self.biomedical_concepts += item.usdm_biomedical_concepts
        self.double_link(self.activities, 'previousActivityId', 'nextActivityId')
        
        prev_instance = None
        for raw_timepoint in self._raw_timepoints.items:
          instance = raw_timepoint.usdm_timepoint
          instance.defaultConditionId = None
          instances.append(instance)
          if prev_instance is not None:
            prev_instance.defaultConditionId = instance.id
          prev_instance = instance
        exit = self._add_exit()
        instance.scheduleTimelineExitId = exit.id
        self.timeline = self._add_timeline(self.name, self.description, self.condition, instances, exit)

    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet")
      self._traceback(f"{traceback.format_exc()}")

  def _process_sheet(self):
    for rindex in range(self.NAME_ROW, self.CONDITION_ROW + 1):
      if rindex == self.NAME_ROW:
        self.name = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.DESCRIPTION_ROW:
        self.description = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.CONDITION_ROW:
        self.condition = self.read_cell(rindex, self.PARAMS_DATA_COL)
      else:
        pass

  def _add_exit(self):
    exit =  ScheduleTimelineExit(id=id_manager.build_id(ScheduleTimelineExit))
    cross_references.add(exit.id, exit)
    return exit

  def _add_timeline(self, name, description, condition, instances, exit):
    return ScheduleTimeline(
      id=id_manager.build_id(ScheduleTimeline),
      mainTimeline=self.main_timeline,
      name=name,
      description=description,
      label=name,
      entryCondition=condition,
      scheduleTimelineEntryId=instances[0].id,
      scheduleTimelineExits=[exit],
      scheduleTimelineInstances=instances
    )

  def _link_instance_to_activities(self):
    for timepoint in self._raw_timepoints.items:
      if timepoint.has_activities:
        for activity_name, selected in timepoint.activity_map.items():
          if selected:
            activity = self._raw_activities.item_by_name(activity_name)
            timepoint.add_activity(activity)

  def _insert_cycles_into_timeline(self):
    cycle_offset = 0
    for cycle in self._raw_cycles.items:
      start_index = cycle.start_timepoint_index + cycle_offset
      self._raw_timepoints.insert_at(start_index, 'anchor', cycle.start, cycle.cycle)
      cycle_offset += 1

      end_index = cycle.end_timepoint_index + cycle_offset + 1
      self._raw_timepoints.insert_at(end_index, 'previous', cycle.period, None)
      cycle_offset += 1

      if cycle.end_rule != "":
        end_index = cycle.end_timepoint_index + cycle_offset + 1
        self._raw_timepoints.insert_at(end_index, 'condition', cycle.end_rule, None, start_index)
        cycle_offset += 1

