import logging
from yattag import Doc
from usdm_db.cross_reference import CrossReference
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging
from usdm_model.scheduled_instance import (
    ScheduledActivityInstance,
    ScheduledDecisionInstance,
    ScheduledInstance,
)
from usdm_model.schedule_timeline_exit import ScheduleTimelineExit


class Timeline:
    FULL = "full"
    BODY = "body"

    def __init__(self, study):
        self._errors_and_logging = ErrorsAndLogging()
        self._study = study
        self._cross_ref = CrossReference(study, self._errors_and_logging)

    def to_html(self, level=FULL):
        try:
            doc = Doc()
            study_design = self._study.versions[0].studyDesigns[0]
            if level == self.BODY:
                self._body(doc, study_design)
            else:
                self._full(doc, study_design)
            return doc.getvalue()
        except Exception as e:
            self._errors_and_logging.exception(
                f"Failed generating HTML page at level '{level}'", e
            )

    def _full(self, doc, study_design):
        doc.asis("<!DOCTYPE html>")
        with doc.tag("html"):
            with doc.tag("head"):
                pass
            with doc.tag("body"):
                self._body(doc, study_design)

    def _body(self, doc, study_design):
        for timeline in study_design.scheduleTimelines:
            timings = timeline.timings
            with doc.tag(f"h1"):
                doc.asis(f"{timeline.name}")
            with doc.tag("pre", klass="mermaid"):
                doc.asis("\ngraph LR\n")
                doc.asis(f"{timeline.id}([{timeline.entryCondition}])\n")
                instance = self._cross_ref.get(
                    ScheduledActivityInstance, timeline.entryId
                )
                if instance.instanceType == ScheduledActivityInstance.__name__:
                    doc.asis(f"{instance.id}(ScheduledActivityInstance)\n")
                else:
                    doc.asis(f"{instance.id}{{{{ScheduledDecisionInstance}}}}\n")
                doc.asis(f"{timeline.id} -->|first| {instance.id}\n")
                prev_instance = instance
                instance = self._cross_ref.get(
                    ScheduledActivityInstance, instance.defaultConditionId
                )
                while instance:
                    if instance.instanceType == ScheduledActivityInstance.__name__:
                        doc.asis(f"{instance.id}(ScheduledActivityInstance)\n")
                    else:
                        doc.asis(f"{instance.id}{{{{ScheduledDecisionInstance}}}}\n")
                        for condition in instance.conditionAssignments:
                            doc.asis(
                                f"{instance.id} -->|{condition.condition}| {condition.conditionTargetId}\n"
                            )
                    doc.asis(f"{prev_instance.id} -->|default| {instance.id}\n")
                    prev_instance = instance
                    instance = self._get_cross_reference(
                        prev_instance.defaultConditionId
                    )
                exit = self._cross_ref.get(
                    ScheduleTimelineExit, prev_instance.timelineExitId
                )
                doc.asis(f"{exit.id}([Exit])\n")
                doc.asis(f"{prev_instance.id} -->|exit| {exit.id}\n")
                for timing in timings:
                    doc.asis(
                        f"{timing.id}(({timing.label}\n{timing.type.decode}\n{timing.value}\n{timing.windowLower}..{timing.windowUpper}))\n"
                    )
                    doc.asis(
                        f"{timing.id} -->|from| {timing.relativeFromScheduledInstanceId}\n"
                    )
                    doc.asis(
                        f"{timing.id} -->|to| {timing.relativeToScheduledInstanceId}\n"
                    )
        with doc.tag("script", type="module"):
            doc.asis(
                "import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';\n"
            )
            doc.asis("mermaid.initialize({ startOnLoad: true });\n")

    def _get_cross_reference(self, id):
        for klass in [ScheduledActivityInstance, ScheduledDecisionInstance]:
            instance = self._cross_ref.get(klass, id)
            if instance:
                return instance
        return None
