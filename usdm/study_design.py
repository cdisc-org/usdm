from typing import List, Union
from .activity import Activity
from .api_base_model import ApiBaseModel
from .alias_code import AliasCode
from .biomedical_concept import BiomedicalConcept
from .biomedical_concept_category import BiomedicalConceptCategory
from .biomedical_concept_surrogate import BiomedicalConceptSurrogate
from .code import Code
from .encounter import Encounter
from .study_cell import StudyCell
from .indication import Indication
from .investigational_intervention import InvestigationalIntervention
from .study_design_population import StudyDesignPopulation
from .objective import Objective
from .schedule_timeline import ScheduleTimeline
from .workflow import Workflow
from .workflow_item import WorkflowItem
from .estimand import Estimand
import pandas as pd

class StudyDesign(ApiBaseModel):
  studyDesignId: str
  studyDesignName: str
  studyDesignDescription: str
  trialIntentTypes: List[Code] = []
  trialType: List[Code] = []
  interventionModel: Code
  studyCells: List[StudyCell] = []
  studyIndications: List[Indication] = []
  studyInvestigationalInterventions: List[InvestigationalIntervention] = []
  studyStudyDesignPopulations: List[StudyDesignPopulation] = []
  studyObjectives: List[Objective] = []
  studyScheduleTimelines: List[ScheduleTimeline] = []
  therapeuticAreas: List[Code] = []
  studyEstimands: List[Estimand] = []
  encounters: List[Encounter] = []
  activities: List[Activity] = []
  studyDesignRationale: str
  studyDesignBlindingScheme: AliasCode = None
  biomedicalConcepts: List[BiomedicalConcept] = []
  bcCategories: List[BiomedicalConceptCategory] = []
  bcSurrogates: List[BiomedicalConceptSurrogate] = []

  @classmethod
  def search(cls, store, uuid):
    designs = store.get_by_klass_and_scope("StudyDesign", uuid)
    return designs

class SoA():
  def __init__(self, study_design, store):
    self.study_design = study_design
    self.store = store
    self.encounters = {}
    self.activities_by_desc = {}
    self.activities_by_uuid = {}
    self.encounters_by_uuid = {}
    self.activity_encounter_map = []
    self.epoch_encounter_map = {}
    self.epochs_by_uuid = {}

  def soa(self):
    # Data
    encounter_index = {}
    encounter_rule = []

    self.activity_encounters()
    self.epoch_encounters()
    activities_io = self.activities_in_order()
    encounters_io = self.encounters_in_order()

    for idx, encounter in enumerate(encounters_io):
        encounter_index[encounter] = idx

    # Encounter Rules
    result = self.encounter_rules()
    for name, record in result.items():
      if record["start_rule"] == record["end_rule"]:
        encounter_rule.append("%s" % (record["start_rule"]))
      else:
        encounter_rule.append("%s to %s" % (record["start_rule"], record["end_rule"]))

    # Activities
    activities = {}
    for record in self.activity_encounter_map:
      if not record['activity'] in activities:
        activities[record['activity']] = [''] * len(encounters_io)
      activities[record['activity']][encounter_index[record["encounter"]]] = "X" 

    rows = []
    rows.append([""] + list(self.epoch_encounter_map.values()))
    rows.append([""] + list(encounters_io))
    rows.append([""] + list(encounter_rule))
    for activity in activities_io:
      if activity in activities:
        data = activities[activity]
        rows.append([activity] + list(data))
    n = len(rows[0])
    for row in rows:
      print("ROW:", row)
    df = pd.DataFrame(rows, columns=list(range(n)))
    print(df.to_string())
    return df

  def activity_encounters(self):
    wf = Workflow.read(self.store, str(self.study_design.studyWorkflows[0]))
    for wfi_uuid in wf['workflowItems']:
      wfi = WorkflowItem.read(self.store, wfi_uuid)
      encounter_uuid = wfi['workflowItemEncounter']
      activity_uuid = wfi['workflowItemActivity']
      activity = self.store.get("", activity_uuid)
      encounter = self.store.get("", encounter_uuid)
      encounter_name = encounter['encounterName']
      activity_desc = activity['activityDesc']
      self.encounters_by_uuid[encounter_uuid] = encounter
      self.activities_by_desc[activity_desc] = activity
      self.activities_by_uuid[activity_uuid] = activity
      self.activity_encounter_map.append({ 'encounter': encounter_name, 'activity': activity_desc })

  def epoch_encounters(self):
    cells = self.store.get_by_klass("StudyCell")
    for cell in cells:
      if cell['uuid'] in map(str, self.study_design.studyCells):
        epoch_uuid = cell['studyEpoch']
        epoch = self.store.get("", epoch_uuid)
        epoch_name = epoch['studyEpochName']
        for encounter_uuid in epoch['encounters']:
          encounter = self.store.get("", encounter_uuid)
          encounter_name = encounter['encounterName']
          self.epoch_encounter_map[encounter_name] = epoch_name
          self.epochs_by_uuid[epoch['uuid']] = epoch

  def encounter_rules(self):
    the_encounters = {}
    for encounter in self.encounters_by_uuid.values():
      encounter_name = encounter['encounterName']
      start_rule_uuid = encounter['transitionStartRule']
      end_rule_uuid = encounter['transitionEndRule']
      record = { 
        'encounter': encounter_name, 
        'start_rule': self.get_rule(start_rule_uuid), 
        'end_rule': self.get_rule(end_rule_uuid) 
      }
      the_encounters[encounter_name] = record
    return the_encounters

  def get_rule(self, uuid):
    if uuid == None:
      return ""
    rule = self.store.get("", uuid)['transitionRuleDesc']
    return rule

  def activities_in_order(self):
    return self.in_order(self.activities_by_uuid, 'activityDesc', 'previousActivityId', 'nextActivityId')

  def encounters_in_order(self):
    return self.in_order(self.encounters_by_uuid, 'encounterName', 'previousEncounterId', 'nextEncounterId')

  def in_order(self, collection, key_field, prev_field, next_field):
    next_item = self.first_in_list(collection, prev_field)
    result_map = {}
    ordinal = 1
    more = True
    while more:
      key = next_item[key_field]
      result_map[key] = int(ordinal)
      ordinal += 1
      next_uuid = next_item[next_field]
      if next_uuid == None:
        more = False
      else:
        next_item = collection[next_uuid]
    ordered = self.order_dict(result_map)
    return ordered.keys()

  def first_in_list(self, collection, field_name):
    for item in collection.values():
      if item[field_name] == None:
        return item
    return None

  def order_dict(self, the_dict):
    return { k: the_dict[k] for k in sorted(the_dict, key=the_dict.get) }