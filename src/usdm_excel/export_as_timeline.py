from yattag import Doc
from usdm_excel.cross_ref import cross_references
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_model.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance, ScheduledInstance
from usdm_model.schedule_timeline_exit import ScheduleTimelineExit
import traceback

class ExportAsTimeline():

  def __init__(self, study):
    self.study = study

  def export(self):
    doc = Doc()
    study_design = self.study.studyDesigns[0]
    try:
      doc.asis('<!DOCTYPE html>')
      with doc.tag('html'):
        with doc.tag('head'):
          pass
        with doc.tag('body'):
          for timeline in study_design.studyScheduleTimelines:
            timings = []
            with doc.tag(f'h1'):
              doc.asis(f'Timeline {timeline.id}')
            with doc.tag('pre', klass='mermaid'):
              doc.asis('\ngraph LR\n')
              doc.asis(f'{timeline.id}([{timeline.entryCondition}])\n')
              instance = cross_references.get_by_id(ScheduledActivityInstance, timeline.scheduleTimelineEntryId)
              if instance.instanceType == 'ACTIVITY': 
                doc.asis(f'{instance.id}(A)\n')
              else:
                doc.asis(f'{instance.id}{{{{D}}}}\n')
              doc.asis(f'{timeline.id} -->|first| {instance.id}\n')
              for timing in instance.scheduledInstanceTimings:
                #print(f"APPEND: {timing}")
                timings.append(timing)
              prev_instance = instance
              instance = cross_references.get_by_id(ScheduledActivityInstance, instance.defaultConditionId)
              while instance:
                #print(f"INST: {instance}")
                if instance.instanceType == 'ACTIVITY': 
                  doc.asis(f'{instance.id}(A)\n')
                else:
                  doc.asis(f'{instance.id}{{{{D}}}}\n')
                  for condition in instance.conditionAssignments:
                    doc.asis(f'{instance.id} -->|{condition[0]}| {condition[1]}\n') 
                doc.asis(f'{prev_instance.id} -->|default| {instance.id}\n')      
                for timing in instance.scheduledInstanceTimings:
                  #print(f"APPEND: {timing}")
                  timings.append(timing)
                prev_instance = instance
                instance = self._get_cross_reference(prev_instance.defaultConditionId)
                #print(f"NEXT: {instance}")
              exit = cross_references.get_by_id(ScheduleTimelineExit, prev_instance.scheduleTimelineExitId)
              doc.asis(f'{exit.id}([Exit])\n')
              doc.asis(f'{prev_instance.id} -->|exit| {exit.id}\n')      
              for timing in timings:
                #print(f"TIMING: {timing}")
                doc.asis(f'{timing.id}(({timing.label}\n{timing.type.decode}\n{timing.timingValue}\n{timing.timingWindowLower}..{timing.timingWindowUpper}))\n')            
                doc.asis(f'{timing.id} -->|from| {timing.relativeFromScheduledInstanceId}\n')      
                doc.asis(f'{timing.id} -->|to| {timing.relativeToScheduledInstanceId}\n')      
          with doc.tag('script', type='module'):
            doc.asis("import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';\n")   
            doc.asis("mermaid.initialize({ startOnLoad: true });\n")   
    except:
      print(f"{traceback.format_exc()}")
    return doc.getvalue()

  def _get_cross_reference(self, id):
    for klass in [ScheduledActivityInstance, ScheduledDecisionInstance]:
      instance = cross_references.get_by_id(klass, id)
      if instance:
        return instance 
    return None

