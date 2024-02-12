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

  def _timing_from(self, timings, sai):
    return next((item for item in timings if item.relativeFromScheduledInstanceId == sai.id), None)

  def _condition_no_context(self, conditions, target):
    return next((item for item in conditions if target.id in item.appliesToIds and not item.contextIds), None)

  def _condition_with_context(self, conditions, target, context):
    return next((item for item in conditions if target.id in item.appliesToIds and context.id in item.contextIds), None)

  def _template_copy(self, template):
    result = []
    for item in template:
      result.append(item.copy())
    return result
        
  def generate(self):

    # ScheduleActivityInstance order
    required_activities = []
    sai_order = []
    item = self._find(self.timeline.instances, self.timeline.entryId)
    more = True
    while more:
      sai_order.append(item)
      for id in item.activityIds:
        if id not in required_activities:
          required_activities.append(id)
      more = False if not item.defaultConditionId else True
      item = self._find(self.timeline.instances, item.defaultConditionId)
    #print(f"SAI ORDER: {sai_order}\n\n")
    #print(f"ACTIVITIES: {required_activities}\n\n")

    # Activity order
    activity_order = []
    item = self._first(self.study_design.activities)
    more = True
    while more:
      #print(f"ACTIVITY CHECK: {item.id}\n\n")
      if item.id in required_activities:
        activity_order.append(item)
      more = False if not item.nextId else True
      item = self._find(self.study_design.activities, item.nextId)
    #print(f"ACTIVITY ORDER: {activity_order}\n\n")

    row_template = []
    lh_columns = ['activity']
    sai_start_index = len(lh_columns)
    for item in lh_columns:
      row_template.append({'label': ''})
    for sai in enumerate(sai_order):
      row_template.append({'label': ''})

    results = []

    row = self._template_copy(row_template)
    for index, sai in enumerate(sai_order):
      row[index + sai_start_index]['label'] = index
    results.append(row)

    row = self._template_copy(row_template)
    
    for index, sai in enumerate(sai_order):
      if sai.epochId:
        item = cross_references.get_by_id("StudyEpoch", sai.epochId)
        row[index + sai_start_index]['label'] = item.label if item else "???"
        #row[index + sai_start_index] = sai.epochId
    results.append(row)

    row = self._template_copy(row_template)
    for index, sai in enumerate(sai_order):
      if sai.encounterId:
        item = cross_references.get_by_id("Encounter", sai.encounterId)
        row[index + sai_start_index]['label'] = item.label if item else "???"
        #row[index + sai_start_index] = sai.encounterId
    results.append(row)

    row = self._template_copy(row_template)
    for index, sai in enumerate(sai_order):
      timing = self._timing_from(self.timeline.timings, sai)
      if timing:
        row[index + sai_start_index]['label'] = timing.label
    results.append(row)

    for activity in activity_order:
      row = self._template_copy(row_template)
      row[0]['label'] = activity.label
      condition = self._condition_no_context(self.study_design.conditions, activity)
      if condition:
        #print(f"COND: {condition}")
        row[0]['condition'] = condition
      for index, sai in enumerate(sai_order):
        row[index + sai_start_index]['set'] = False
        if activity.id in sai.activityIds:
          row[index + sai_start_index]['set'] = True
          condition = self._condition_with_context(self.study_design.conditions, activity, sai)
          if condition:
            row[index + sai_start_index]['condition'] = condition
      results.append(row)

    return results