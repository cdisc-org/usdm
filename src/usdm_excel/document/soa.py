from usdm_excel.cross_ref import cross_references
from usdm_excel.base_sheet import BaseSheet
#from usdm_excel.study_sheet.study_sheet import Study
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_model.activity import Activity
from usdm_model.scheduled_instance import ScheduledActivityInstance, ScheduledDecisionInstance
from usdm_model.study_design import StudyDesign

class SoA():

  def __init__(self, parent: BaseSheet, study_design: StudyDesign, timeline: ScheduleTimeline):
    self.parent = parent
    self.study_design = study_design
    self.timeline = timeline

  def _first(self, collection):
    return next((item for item in collection if not item.previousId), None)

  def _find(self, collection, id):
    return next((item for item in collection if item.id == id), None)

  def simple(self):

    # Activity order
    activity_order = []
    item = self._first(self.study_design.activities)
    more = True
    print("1")
    while more:
      activity_order.append(item)
      print("2")
      more = False if not item.nextId else True
      item = self._find(self.study_design.activities, item.nextId)
    print(f"ACTIVITY ORDER: {activity_order}")
    print("")
    print("")

    # ScheduleActivityInstance order
    sai_order = []
    timeline = self.timeline
    item = self._find(timeline.instances, self.timeline.entryId)
    more = True
    print("3")
    while more:
      sai_order.append(next)
      print("4")
      more = False if not item.defaultConditionId else True
      item = self._find(timeline.instances, item.defaultConditionId)
    print(f"SAI ORDER: {sai_order}")
    print("")
    print("")

    row_template = []
    lh_columns = ['activity']
    sai_start_index = len(lh_columns)
    for item in lh_columns:
      row_template.append('')
    for item in sai_order:
      row_template.append('')

    results = []
    results.append(row_template)

    for activity in activity_order:
      row = row_template.copy()
      row[0] = activity.label
      results.append(row)

    return results