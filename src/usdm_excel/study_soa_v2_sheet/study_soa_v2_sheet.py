from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_v2_sheet.soa_activities import SoAActivities
from usdm_excel.study_soa_v2_sheet.scheduled_instances import ScheduledInstances
from usdm_model.scheduled_instance import (
    ScheduledActivityInstance,
    ScheduledDecisionInstance,
)
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_excel.globals import Globals


class StudySoAV2Sheet(BaseSheet):
    NAME_ROW = 0
    DESCRIPTION_ROW = 1
    CONDITION_ROW = 2
    PARAMS_DATA_COL = 1

    def __init__(
        self,
        file_path: str,
        globals: Globals,
        sheet_name: str,
        main: bool = False,
        require: dict = {},
    ):
        try:
            self.name = ""
            self.description = ""
            self.condition = ""
            self.timeline = None
            self.main_timeline = main
            self.activities = []
            self.biomedical_concepts = []
            self.biomedical_concept_surrogates = []
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=sheet_name,
                header=None,
                require=require,
            )
            self._process_sheet()
            self._raw_activities = SoAActivities(
                self
            )  # Order important, activities then instances
            self._raw_instances = ScheduledInstances(self)
            (
                self.activities,
                self.biomedical_concepts,
                self.biomedical_concept_surrogates,
            ) = self._raw_activities.group_and_link()
            self._raw_activities.set_parents()
            self.timeline = self._add_timeline(
                self.name,
                self.description,
                self.condition,
                self._raw_instances.instances,
                self._raw_instances.exits,
            )

        except Exception as e:
            self._sheet_exception(e)

    def check_timing_references(self, timings, timing_check):
        timing_set = []
        for instance in self._raw_instances.items:
            item = instance.item
            # print(f"TIMING1: {item.id}, {instance.name}")
            if isinstance(item, ScheduledActivityInstance):
                found = False
                for timing in timings:
                    ids = [
                        timing.relativeFromScheduledInstanceId,
                        timing.relativeToScheduledInstanceId,
                    ]
                    # print(f"TIMING2: {timing.name}, {ids}")
                    if item.id in ids:
                        # print(f"TIMING3: found")
                        found = True
                        if not timing_check[timing.name]:
                            timing_check[timing.name] = self.name
                            timing_set.append(timing)
                        elif timing_check[timing.name] == self.name:
                            pass
                        else:
                            self._general_warning(
                                f"Duplicate use of timing with name '{timing.name}' across timelines detected"
                            )
                        # break
                if not found:
                    self._general_warning(
                        f"Unable to find timing reference for instance with name '{instance.name}'"
                    )
        return timing_set

    def timing_match(self, ref):
        return self._raw_instances.match(ref)

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

    def _add_timeline(self, name, description, condition, instances, exit):
        try:
            timeline = ScheduleTimeline(
                id=self.globals.id_manager.build_id(ScheduleTimeline),
                mainTimeline=self.main_timeline,
                name=name,
                description=description,
                label=name,
                entryCondition=condition,
                entryId=instances[0].id,
                exits=exit,
                instances=instances,
            )
            self.globals.cross_references.add(timeline.name, timeline)
            return timeline
        except Exception as e:
            self._general_exception(f"Failed to create ScheduleTimeline object", e)
            return None
