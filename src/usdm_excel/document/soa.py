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
    while more:
      activity_order.append(item)
      more = False if not item.nextId else True
      item = self._find(self.study_design.activities, item.nextId)
    print(f"ACTIVITY ORDER: {activity_order}\n\n")

    # ScheduleActivityInstance order
    sai_order = []
    timeline = self.timeline
    item = self._find(timeline.instances, self.timeline.entryId)
    more = True
    while more:
      sai_order.append(item)
      more = False if not item.defaultConditionId else True
      item = self._find(timeline.instances, item.defaultConditionId)
    print(f"SAI ORDER: {sai_order}\n\n")

    row_template = []
    lh_columns = ['activity']
    sai_start_index = len(lh_columns)
    for item in lh_columns:
      row_template.append('')
    for sai in enumerate(sai_order):
      row_template.append(f'')

    results = []

    row = row_template.copy()
    for index, sai in enumerate(sai_order):
      row[index + sai_start_index] = index
    results.append(row)

    # row = row_template.copy()
    # for index, sai in enumerate(sai_order):
    #   if sai.epochId:
    #     row[index + sai_start_index] = sai.epochId
    # results.append(row)

    row = row_template.copy()
    for index, sai in enumerate(sai_order):
      if sai.encounterId:
        row[index + sai_start_index] = sai.encounterId
    results.append(row)

    for activity in activity_order:
      row = row_template.copy()
      row[0] = activity.label
      for index, sai in enumerate(sai_order):
        if activity.id in sai.activityIds:
          row[index + sai_start_index] = "X"
      results.append(row)

    return results