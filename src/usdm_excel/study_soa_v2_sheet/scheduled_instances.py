from usdm_excel.study_soa_v2_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_v2_sheet.scheduled_instance import ScheduledInstance
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
from usdm_model.schedule_timeline_exit import ScheduleTimelineExit

class ScheduledInstances():
  
  def __init__(self, parent):
    self.parent = parent
    self.items = []
    self.map = {}
    self.exits = []
    self.instances = []
    self._build_instances()
    self._set_default_references()
    self._set_condition_references()

  def _build_instances(self):    
    for col_index in range(self.parent.sheet.shape[1]):
      if col_index >= SoAColumnRows.FIRST_VISIT_COL:
        record = ScheduledInstance(self.parent, col_index)
        self.items.append(record)
        self.map[record.name] = record

  def _set_default_references(self):
    for instance in self.items:
      item = instance.item
      self.instances.append(item)
      if instance.default_name in self.map.keys():
        instance.item.defaultConditionId = self.map[instance.default_name].item.id
      elif instance.default_name.upper() == "(EXIT)":
        exit = self._add_exit()
        instance.item.scheduleTimelineExitId = exit.id
        self.exits.append(exit)
      else:
        self.parent._general_error(f"Default reference from {instance.name} to {instance.default_name} cannot be made, not found on the same timeline")

  def _add_exit(self):
    exit = ScheduleTimelineExit(id=id_manager.build_id(ScheduleTimelineExit))
    cross_references.add(exit.id, exit)
    return exit

  def _set_condition_references(self):
    for instance in self.items:
      item = instance.item
      if item.instanceType == 'CONDITION':
        for condition in instance.conditions.items:
          if condition['name'] in self.map.keys():
            condition.conditionAssignments.append([condition['condition'], self.map[condition['name']].item.id])
          else:
            self.parent._general_error(f"Conditonal reference from {instance.name} to {condition['name']} cannot be made, not found on the same timeline")
  
  # def _set_to_timing_refs(self):    
  #   for item in self.items:
  #     from_instance = item.usdm_timepoint
  #     from_timing = from_instance.scheduledInstanceTimings[0]
  #     from_timing_type = from_timing.type.code
  #     if from_timing_type == "ANCHOR":
  #       continue
  #     to_instance = self.items[item.reference].usdm_timepoint
  #     from_timing.relativeToScheduledInstanceId = to_instance.id