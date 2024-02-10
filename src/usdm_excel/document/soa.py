#from usdm_excel.cross_ref import cross_references
from usdm_excel.base_sheet import BaseSheet
#from usdm_excel.study_sheet.study_sheet import Study
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_model.study_design import StudyDesign

class SoA():

  def __init__(self, parent: BaseSheet, study_design: StudyDesign, timeline: ScheduleTimeline):
    self.parent = parent
    self.study_design = study_design
    self.timeline = timeline

  def _first(self, collection):
    return next((item for item in collection if not item.previous), None)

  def _find_sai(self, id):
    return next((item for item in self.timeline if item.id == id), None)

  def simple(self):

    # Activity order
    activity_order = []
    next = self._first(self.study_design.activities)
    more = True
    while more:
      activity_order.append(next)
      more = False if not next.nextId else True
    print(f"ACTIVITY ORDER: {activity_order}")
    print("")
    print("")

    # ScheduleActivityInstance order
    sai_order = []
    next = self._find_sai(self.timeline.entryId)
    more = True
    while more:
      sai_order.append(next)
      more = False if not next.nextId else True
      next = self._find_sai(next.defaultConditionId)
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