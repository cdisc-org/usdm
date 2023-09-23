from yattag import Doc
from usdm_excel.cross_ref import cross_references
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_model.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance, ScheduledInstance

class ExportAsTimeline():

  def __init__(self, study):
    self.study = study

  def export(self):
    doc = Doc()
    study_design = self.study.studyDesigns[0]
    doc.asis('<!DOCTYPE html>')
    with doc.tag('html'):
      with doc.tag('head'):
        pass
      with doc.tag('body'):
        for timeline in study_design.studyScheduleTimelines:
          with doc.tag(f'h1'):
            doc.asis(f'Timeline {timeline.id}')
          with doc.tag('pre', klass='mermaid'):
            doc.asis('\ngraph LR\n')
            doc.asis(f'{timeline.id}([{timeline.entryCondition}])\n')
            instance = cross_references.get_by_id(ScheduledActivityInstance, timeline.scheduleTimelineEntryId)
            if instance.instanceType == 'ACTIVITY': 
              doc.asis(f'{instance.id}({instance.id})\n')
            else:
              doc.asis(f'{instance.id}{{{{{instance.id}}}}}\n')
            doc.asis(f'{timeline.id} --> {instance.id}')
        with doc.tag('script', type='module'):
          doc.asis("import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';\n")   
          doc.asis("mermaid.initialize({ startOnLoad: true });\n")   
    return doc.getvalue()

