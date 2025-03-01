from .utility import usdm_reference
from usdm_excel.base_sheet import BaseSheet
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_model.study_design import StudyDesign
from usdm_model.study_version import StudyVersion


class SoA:
    def __init__(
        self,
        parent: BaseSheet,
        study_version: StudyVersion,
        study_design: StudyDesign,
        timeline: ScheduleTimeline,
    ):
        self.parent = parent
        self.study_version = study_version
        self.study_design = study_design
        self.timeline = timeline

    def _first(self, collection):
        return next((item for item in collection if not item.previousId), None)

    def _find(self, collection, id):
        return next((item for item in collection if item.id == id), None)

    def _timing_from(self, timings, sai):
        return next(
            (
                item
                for item in timings
                if item.relativeFromScheduledInstanceId == sai.id
            ),
            None,
        )

    def _condition_no_context(self, conditions, target):
        return next(
            (
                item
                for item in conditions
                if target.id in item.appliesToIds and not item.contextIds
            ),
            None,
        )

    def _condition_with_context(self, conditions, target, context):
        return next(
            (
                item
                for item in conditions
                if target.id in item.appliesToIds and context.id in item.contextIds
            ),
            None,
        )

    def _template_copy(self, template):
        result = []
        for item in template:
            result.append(item.copy())
        return result

    def _has_non_empty(self, the_list):
        return any(s["label"] != "" for s in the_list)

    def generate(self):
        # ScheduleActivityInstance order
        required_activities = []
        sai_order = []
        item = self._find(self.timeline.instances, self.timeline.entryId)
        more = True
        while more:
            sai_order.append(item)
            if hasattr(item, "activityIds"):
                for id in item.activityIds:
                    if id not in required_activities:
                        required_activities.append(id)
            more = False if not item.defaultConditionId else True
            item = self._find(self.timeline.instances, item.defaultConditionId)
        # print(f"SAI ORDER: {sai_order}\n\n")
        # print(f"ACTIVITIES: {required_activities}\n\n")

        # Activity order
        activity_order = []
        item = self._first(self.study_design.activities)
        more = True
        while more:
            # print(f"ACTIVITY CHECK: {item.id}\n\n")
            if item.id in required_activities:
                activity_order.append(item)
            more = False if not item.nextId else True
            item = self._find(self.study_design.activities, item.nextId)
        # print(f"ACTIVITY ORDER: {activity_order}\n\n")

        row_template = []
        lh_columns = ["activity"]
        sai_start_index = len(lh_columns)
        for item in lh_columns:
            row_template.append({"label": ""})
        for sai in enumerate(sai_order):
            row_template.append({"label": ""})

        results = []

        # row = self._template_copy(row_template)
        # for index, sai in enumerate(sai_order):
        #   row[index + sai_start_index]['label'] = index
        # results.append(row)

        row = self._template_copy(row_template)
        for index, sai in enumerate(sai_order):
            if sai.epochId:
                item = self.parent.globals.cross_references.get_by_id(
                    "StudyEpoch", sai.epochId
                )
                row[index + sai_start_index]["label"] = (
                    usdm_reference(item, "label") if item else "???"
                )
        if self._has_non_empty(row):
            results.append(row)

        row = self._template_copy(row_template)
        for index, sai in enumerate(sai_order):
            if hasattr(sai, "encounterId"):
                if sai.encounterId:
                    item = self.parent.globals.cross_references.get_by_id(
                        "Encounter", sai.encounterId
                    )
                    row[index + sai_start_index]["label"] = (
                        usdm_reference(item, "label") if item else "???"
                    )
        if self._has_non_empty(row):
            results.append(row)

        row = self._template_copy(row_template)
        for index, sai in enumerate(sai_order):
            timing = self._timing_from(self.timeline.timings, sai)
            if timing:
                row[index + sai_start_index]["label"] = usdm_reference(timing, "label")
        if self._has_non_empty(row):
            results.append(row)

        row = self._template_copy(row_template)
        for index, sai in enumerate(sai_order):
            timing = self._timing_from(self.timeline.timings, sai)
            if timing:
                row[index + sai_start_index]["label"] = usdm_reference(
                    timing, "windowLabel"
                )
        if self._has_non_empty(row):
            results.append(row)

        for activity in activity_order:
            row = self._template_copy(row_template)
            row[0]["label"] = usdm_reference(activity, "label")
            condition = self._condition_no_context(
                self.study_version.conditions, activity
            )
            if condition:
                row[0]["condition"] = condition
            for index, sai in enumerate(sai_order):
                row[index + sai_start_index]["set"] = False
                if hasattr(sai, "activityIds"):
                    if activity.id in sai.activityIds:
                        row[index + sai_start_index]["set"] = True
                        condition = self._condition_with_context(
                            self.study_version.conditions, activity, sai
                        )
                        if condition:
                            row[index + sai_start_index]["condition"] = condition
            results.append(row)

        return results
