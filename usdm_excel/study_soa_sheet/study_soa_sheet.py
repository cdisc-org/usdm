from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import IdManager
import traceback
import pandas as pd

class StudySoASheet(BaseSheet):

  EPOCH_ROW = 0
  CYCLE_ROW = 1
  CYCLE_START_ROW = 2
  CYCLE_PERIOD_ROW = 3
  CYCLE_END_RULE_ROW = 4
  TIMING_ROW = 5
  VISIT_LABEL_ROW = 6
  VISIT_WINDOW_ROW = 7

  HEADER_ROW = 8
  FIRST_ACTIVITY_ROW = 9

  ACTIVITY_COL = 0
  CHILD_ACTIVITY_COL = 1
  BC_COL = 2
  FIRST_VISIT_COL = 3

  def __init__(self, file_path, id_manager: IdManager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='soa', header=None), id_manager)
      self.timelines = []
      #self.epoch_encounter_map = {}
      #self.activity_map = {}
      self.row_activities_map = []
      self.activity_bc_map = {}
      self.sheet = self.sheet.fillna(method='ffill', axis=1)
      self.cycles = self.extract_cycles()
      self.timepoints = self.extract_timepoints()
      self.encounters = self.extract_encounters()
      self.activity_bc_map, self.row_activities_map, self.activities = self.extract_activities_and_bcs()
      self.tp_activities = self.extract_timepoint_activities_map()

      self.process_sheet()
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()

  def get_cycle_cell(self, row_index, col_index):
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return "", True
    else:
      value = str(self.sheet.iloc[row_index, col_index])
      if value.upper() == "-":
        return "", True
      else:
        return value, False

  def previous_index(index):
    if index == 0:
      return 0
    else:
      return index - 1

  def build_cycle_record(self, index, col_index, cycle):
    cycle_start_index = index
    cycle_start, is_null = self.get_cycle_cell(self.CYCLE_START_ROW, col_index)
    cycle_period, is_null = self.get_cycle_cell(self.CYCLE_PERIOD_ROW, col_index)
    cycle_end_rule, is_null = self.get_cycle_cell(self.CYCLE_END_RULE_ROW, col_index)
    return { 
      'start_index': cycle_start_index, 
      'cycle': cycle, 
      'start': cycle_start, 
      'period': cycle_period, 
      'end_rule': cycle_end_rule 
    }

  def extract_cycles(self):
    cycles = []
    timepoint_index = -1
    cycle_start_index = None
    in_cycle = False
    prev_cycle = None
    for col_index in range(self.sheet.shape[1]):
      if col_index >= self.FIRST_VISIT_COL:
        timepoint_index += 1
        cycle, cycle_is_null = self.get_cycle_cell(self.CYCLE_ROW, col_index)
        if cycle_is_null:
          if in_cycle:
            cycle_record['end_index'] = self.previous_index(timepoint_index)
            cycles.append(cycle_record)
            in_cycle = False
          else:
            pass # Do nothing
        else:
          cycle = str(cycle)
          if not in_cycle:
            in_cycle = True
            cycle_record = self.build_cycle_record(timepoint_index, col_index, cycle)
          elif prev_cycle == cycle:
            pass # Do nothing
          else:
            cycle_record['end_index'] = self.previous_index(timepoint_index)
            cycles.append(cycle_record)
            cycle_record = self.build_cycle_record(timepoint_index, col_index, cycle)
        prev_cycle = cycle
    return cycles

  def get_timing_cell(self, row_index, col_index):
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return "", True
    else:
      return self.sheet.iloc[row_index, col_index], False

  def get_activity_cell(self, row_index, col_index):
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return "", True
    else:
      value = self.sheet.iloc[row_index, col_index]
      if value == '-':
        return "", True
      else:
        return self.sheet.iloc[row_index, col_index], False
  
  def get_observation_cell(self, row_index, col_index):
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return "", "", True
    else:
      value = self.sheet.iloc[row_index, col_index]
      if value == '-':
        return "", "", True
      else:
        parts = value.split(':')
        if parts[0].lower() == "bc":
          return "bc", parts[1], False
        else:
          return "", "", True

  def get_relative_ref(self, part):
    if len(part) > 1:
      return int(part[1:])
    else:
      return 1

  def get_timing_type(self, col_index):
    timing_type = ""
    rel_ref = 0
    timing_value = ""
    timing_info, timing_info_is_null = self.get_timing_cell(self.TIMING_ROW, col_index)
    if not timing_info_is_null:
      timing_parts = timing_info.split(":")
      if timing_parts[0].upper()[0] == "A":
        timing_type = "anchor"
        rel_ref = 0
      if timing_parts[0].upper()[0] == "P":
        timing_type = "previous"
        rel_ref = self.get_relative_ref(timing_parts[0]) * -1
      elif timing_parts[0].upper()[0] == "N":
        timing_type = "next"
        rel_ref = self.get_relative_ref(timing_parts[0])
      elif timing_parts[0].upper()[0] == "C":
        timing_type = "cycle start"
        rel_ref = self.get_relative_ref(timing_parts[0])
      if len(timing_parts) == 2:
        timing_value = timing_parts[1].strip()
    #print("TIMING: col_index (%s) - FIRST_VISIT_COL (%s) + rel_ref (%s)" % (col_index, FIRST_VISIT_COL, rel_ref))
    return { 'type': timing_type, 'ref': col_index - self.FIRST_VISIT_COL + rel_ref, 'value': timing_value, 'cycle': None }

  def extract_timepoints(self):
    timepoints = []
    for col_index in range(self.sheet.shape[1]):
      if col_index >= self.FIRST_VISIT_COL:
        record = self.get_timing_type(col_index)
        timepoints.append(record)
    return timepoints

  def get_encounter_cell(self, row_index, col_index):
    is_null = pd.isnull(self.sheet.iloc[row_index, col_index])
    if is_null:
      return "", True
    else:
      return self.sheet.iloc[row_index, col_index], False

  def get_encounter_details(self, col_index):
    label = ""
    window = ""
    label, label_is_null = self.get_encounter_cell(self.VISIT_LABEL_ROW, col_index)
    window, window_is_null = self.get_encounter_cell(self.VISIT_WINDOW_ROW, col_index)
    return { 'label': label, 'window': window }

  def extract_encounters(self):
    encounters = []
    for col_index in range(self.sheet.shape[1]):
      if col_index >= self.FIRST_VISIT_COL:
        record = self.get_encounter_details(col_index)
        encounters.append(record)
    return encounters

  def extract_activities_and_bcs(self):
    activity_bc_map = {}
    row_activities_map = []
    activities = []
    prev_activity = None
    for row_index, col_def in self.sheet.iterrows():
      if row_index >= self.FIRST_ACTIVITY_ROW:
        activity, activity_is_null = self.get_activity_cell(row_index, self.CHILD_ACTIVITY_COL)
        if activity_is_null:
          if not prev_activity == None:
            row_activities_map.append(prev_activity)
            activity = prev_activity
        else:
          activities.append(activity)
          row_activities_map.append(activity)
        prev_activity = activity
        obs_type, obs_name, obs_is_null = self.get_observation_cell(row_index, self.BC_COL)
        if not obs_is_null:
          if obs_type == "bc":
            if not activity in activity_bc_map:
              activity_bc_map[activity] = { 'bc': [] }  
            activity_bc_map[activity]['bc'].append(obs_name)
    return activity_bc_map, row_activities_map, activities
  
  def extract_timepoint_activities_map(self):
    timepoint_activity_map = []
    activity_dict = {}
    for activity in self.activities:
      activity_dict[activity] = False
    for tp in self.timepoints:
      timepoint_activity_map.append(dict(activity_dict))
    for index in range(self.sheet.shape[1]):
      if index >= self.FIRST_VISIT_COL:
        column = self.sheet.iloc[:, index]
        row = 0
        for col in column:
          if row >= self.FIRST_ACTIVITY_ROW:
            if not pd.isnull(col):
              if col.upper() == "X":
                print("RA", self.row_activities_map, row)
                activity = self.row_activities_map[row - self.FIRST_ACTIVITY_ROW]
                tp_index = index - self.FIRST_VISIT_COL
                timepoint_activity_map[tp_index][activity] = True
          row += 1
    return timepoint_activity_map

  def process_sheet(self):
    tps = []
    acts = []
    encs = []
    bcs = []
    acts_map = {}
    timing = []
    cycle_offset = 0
    for index, timepoint in enumerate(self.timepoints):
      timepoint['activity_index'] = index
      timepoint['encounter_index'] = index
    for cycle in self.cycles:
      start_index = cycle['start_index'] + cycle_offset
      self.timepoints.insert(start_index, { 'type': 'anchor', 'ref': 0, 'value': cycle['start'], 'activity_index': None, 'encounter_index': None, 'cycle': cycle['cycle'] })
      cycle_offset += 1
      end_index = cycle['end_index'] + cycle_offset + 1
      self.timepoints.insert(end_index, { 'type': 'previous', 'ref': end_index - 1, 'value': cycle['period'], 'activity_index': None, 'encounter_index': None, 'cycle': None })
      cycle_offset += 1
      end_index = cycle['end_index'] + cycle_offset + 1
      self.timepoints.insert(end_index, { 'type': 'condition', 'ref': start_index , 'value': cycle['end_rule'], 'activity_index': None, 'encounter_index': None, 'cycle': None })
      cycle_offset += 1
    previous_tp_id = None
    for activity in self.activities:
      a_bcs = []
      if activity in self.activity_bc_map:
        for a in self.activity_bc_map[activity]['bc']:
          bc = self.json_engine.add_biomedical_concept_surrogate(a, a, "")
          a_bcs.append(bc['bcSurrogateId'])
          bcs.append(bc)
      acts.append(self.json_engine.add_activity(activity, activity, False, "", a_bcs))
      acts_map[activity] = acts[-1]['activityId']
    for encounter in self.encounters:
      encs.append(self.json_engine.add_encounter(encounter['label'], encounter['label'], None, None, []))
    for timepoint in self.timepoints:
      activity_ids = []
      encounter_id = None
      if not timepoint['activity_index'] == None:
        source = self.tp_activities[timepoint['activity_index']]
        for k, v in source.items():
          if v:
            activity_ids.append(acts_map[k])
      if not timepoint['encounter_index'] == None:
        encounter_id = encs[timepoint['encounter_index']]['encounterId']
      tps.append(self.json_engine.add_timepoint(previous_tp_id, None, activity_ids, encounter_id))
      previous_tp_id = tps[-1]['timepointId']
    for index, timepoint in enumerate(self.timepoints):
      if timepoint['type'] == 'condition':
        tps[index]['cycleId'] = tps[timepoint['ref']]['timepointId']
        tps[index]['_type'] = 'Condition'
    for timepoint in self.timepoints:
      if timepoint['type'] == 'next':
        timing.append(self.json_engine.add_next_timing(timepoint['value'], 'StartToStart', None, tps[timepoint['ref']]['timepointId']))
      elif timepoint['type'] == 'previous':
        timing.append(self.json_engine.add_previous_timing(timepoint['value'], 'StartToStart', None, tps[timepoint['ref']]['timepointId']))
      elif timepoint['type'] == 'anchor':
        timing.append(self.json_engine.add_anchor_timing(timepoint['value'], timepoint['cycle']))
      elif timepoint['type'] == 'condition':
        #timing.append(self.json_engine.add_condition_timing(timepoint['value']))
        timing.append({})
      elif timepoint['type'] == 'cycle start':
        timing.append(self.json_engine.add_cycle_start_timing(timepoint['value']))
      elif timepoint['type'] == '':
        timing.append({})
    for index, tp in enumerate(tps):
      tp['scheduledAt'] = timing[index]
    entry = self.json_engine.add_entry('Main timeline', tps[0]['timepointId'])
    exit = self.json_engine.add_exit()
    tps[-1]['exit'] = exit
    self.timelines.append(self.json_engine.add_timeline(entry, tps, exit))
    
  # def process_sheet(self):
  #   #print("SIZE %s x %s" % (self.sheet.shape[0], len(self.sheet.columns)))
  #   wfi_index = 1
  #   for rindex, row in self.sheet.iterrows():
  #     for cindex in range(0, len(self.sheet.columns)):
  #       #print("A %s %s" % (rindex, cindex))  
  #       cell = self.clean_cell_unnamed(rindex, cindex)
  #       #print("CELL [%s,%s] %s" % (rindex, cindex, cell))
  #       if rindex == 0:
  #         pass
  #       elif rindex == 1:
  #         if cindex != 0:
  #           epoch = self.clean_cell_unnamed(rindex - 1, cindex)
  #           description = self.clean_cell_unnamed(rindex + 1, cindex)
  #           encounter = Encounter(uuid=str(uuid4()), encounterName=cell, encounterDesc=description)
  #           if not epoch in self.epoch_encounter_map:
  #             self.epoch_encounter_map[epoch] = []
  #           self.epoch_encounter_map[epoch].append(encounter)
  #           self.encounters.append(encounter)
  #       elif rindex == 2:
  #         pass
  #       else:
  #         if cindex == 0:
  #           activity = Activity(uuid=str(uuid4()), activityName=cell, activityDesc=cell)
  #           self.activity_map[cell] = activity
  #           self.activities.append(activity)
  #         else:
  #           if cell.lower() == "x":
  #             self.workflow_items.append(WorkflowItem(uuid=str(uuid4()), workflowItemDesc="WFI%s" % (wfi_index), workflowItemActivity=self.activities[-1], workflowItemEncounter=self.encounters[cindex-1]))
  #             wfi_index += 1
  #   self.double_link(self.activities, 'uuid', 'previousActivityId', 'nextActivityId')
  #   self.double_link(self.encounters, 'uuid', 'previousEncounterId', 'nextEncounterId')
  #   self.double_link(self.workflow_items, 'uuid', 'previousWorkflowItemId', 'nextWorkflowItemId')

  # def link_study_data(self, study_data_map):
  #   for activity_name, study_data in study_data_map.items():
  #     activity = self.activity_map[activity_name]
  #     activity.studyDataCollection = study_data
