from usdm_excel.study_soa_v2_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_v2_sheet.scheduled_instance import ScheduledInstance

# from usdm_excel.cross_ref import cross_references
# from usdm_excel.id_manager import id_manager
from usdm_model.schedule_timeline_exit import ScheduleTimelineExit
from usdm_model.scheduled_instance import ConditionAssignment


class ScheduledInstances:
    def __init__(self, parent):
        self.parent = parent
        self.items = []
        self.map = {}
        self.exits = []
        self.instances = []
        self._build_instances()
        self._set_default_references()
        self._set_condition_references()

    def match(self, name):
        return self.map[name] if name in self.map else None

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
                instance.item.defaultConditionId = self.map[
                    instance.default_name
                ].item.id
            elif instance.default_name.upper() == "(EXIT)":
                exit = self._add_exit()
                item.timelineExitId = exit.id
                self.exits.append(exit)
            else:
                self.parent._general_error(
                    f"Default reference from {instance.name} to {instance.default_name} cannot be made, not found on the same timeline"
                )

    def _add_exit(self):
        exit = ScheduleTimelineExit(
            id=self.parent.globals.id_manager.build_id(ScheduleTimelineExit)
        )
        self.parent.globals.cross_references.add(exit.id, exit)
        return exit

    def _set_condition_references(self):
        for instance in self.items:
            item = instance.item
            if item.instanceType == "ScheduledDecisionInstance":
                for condition in instance.conditions.items:
                    # print(f"COND: {condition} ")
                    if condition["name"] in self.map.keys():
                        ca = self.parent.create_object(
                            ConditionAssignment,
                            {
                                "condition": condition["condition"],
                                "conditionTargetId": self.map[
                                    condition["name"]
                                ].item.id,
                            },
                        )
                        if ca:
                            item.conditionAssignments.append(ca)
                    else:
                        self.parent._general_error(
                            f"Conditonal reference from {instance.name} to {condition['name']} cannot be made, not found on the same timeline"
                        )
