class DDFJson():
  
  def __init__(self):
    self.id_index = {
      'address': 0,
      'code': 0, 
      'organisation': 0,
      'study_identifier': 0,
      'study_epoch': 0,
      'study_arm': 0,
      'study_cell': 0,
      'entry': 0, 'exit': 0, 'timepoint': 0, 'timeline': 0, 
      'timing': 0, 'study_design': 0, 'study': 0, 'activity': 0, 
      'encounter': 0, 'bc_surrogate': 0 
    }
    self.dicts = {}

  def increment_index(self, name):
    self.id_index[name] += 1

  def build_id(self, name):
    self.increment_index(name)
    return "%s_%s" % (name, self.id_index[name])

  def add_address(self, line, city, district, state, postal_code, country):
    id = self.build_id('address')
    text = "%s, %s, %s, %s, %s, %s" % (line, city, district, state, postal_code, country['decode'])
    result = { '_type': 'Address', 'addressId': id, 'text': text, 'line': line, 'city': city, 'district': district, 'state': state, 'postalCode': postal_code, 'country': country }
    self.dicts[id] = result
    return result

  def add_code(self, code, code_system, code_system_version, decode):
    id = self.build_id('code')
    print("CODE", id)
    result = { '_type': 'Code', 'codeId': id, 'code': code, 'codeSystem': code_system, 'codeSystemVersion': code_system_version, 'decode': decode }
    self.dicts[id] = result
    return result

  def add_organisation(self, scheme, identifier, name, type, address):
    id = self.build_id('organisation')
    result = { '_type': 'Organisation', 'organisationId': id, 'organisationIdentifierScheme': scheme, 'organisationIdentifier': identifier, 'organisationName': name, 'organisationType': type, 'organizationLegalAddress': address }
    self.dicts[id] = result
    return result

  def add_study_identifier(self, identifier, scope):
    id = self.build_id('study_identifier')
    result = { '_type': 'StudyIdentifier', 'studyIdentifierId': id, 'studyIdentifier': identifier, 'studyIdentifierScope': scope }
    self.dicts[id] = result
    return result

  def add_study_epoch(self, name, description):
    id = self.build_id('study_epoch')
    result = { '_type': 'StudyEpoch', 'studyEpochId': id, 'studyEpochName': name, 'studyEpochDescription': description, 'studyEpochType': "", 'previousStudyEpochId': "", 'nextStudyEpochId': "", 'encounters': [] }
    self.dicts[id] = result
    return result

  def add_study_arm(self, name, description):
    id = self.build_id('study_arm')
    result = { '_type': 'StudyArm', 'studyArmId': id, 'studyArmName': name, 'studyArmDescription': description, 'studyArmType': None, 'studyArmDataOriginDescription': "", 'studyArmDataOriginType': None }
    self.dicts[id] = result
    return result

  def add_study_cell(self, arm, epoch):
    id = self.build_id('study_cell')
    result = { '_type': 'StudyCell', 'studyCellId': id, 'studyArm': arm, 'studyEpoch': epoch, 'studyElements': [] }
    self.dicts[id] = result
    return result

  def add_entry(self, description, timepoint_id):
    id = self.build_id('entry')
    result = { '_type': 'Entry', 'entryId': id, 'entryDescription': description, 'nextTimepointId': timepoint_id }
    self.dicts[id] = result
    return result

  def add_exit(self):
    id = self.build_id('exit')
    result = { '_type': 'Exit', 'exitId': id }
    self.dicts[id] = result
    return result

  def add_timepoint(self, previous_timepoint_id, timing, activities, encounter):
    id = self.build_id('timepoint')
    result = { '_type': 'Timepoint', 'timepointId': id, 'nextTimepointId': None, 'scheduledAt': timing, 'timepointActivityIds': activities, 'timepointEncounterId': encounter }
    self.dicts[id] = result
    if not previous_timepoint_id == None:
      self.dicts[previous_timepoint_id]['nextTimepointId'] = id
    return result

  def add_previous_timing(self, value, relative_to_from, window, to_id):
    id = self.build_id('timing')
    result = { '_type': 'Timing', 'timingId': id, 'type': "after", 'value': value, 'relativeToFrom': relative_to_from, 'window': window, 'relativeTo': to_id }
    self.dicts[id] = result
    return result

  def add_next_timing(self, value, relative_to_from, window, to_id):
    id = self.build_id('timing')
    result = { '_type': 'Timing', 'timingId': id, 'type': "next", 'value': value, 'relativeToFrom': relative_to_from, 'window': window, 'relativeTo': to_id }
    self.dicts[id] = result
    return result

  def add_anchor_timing(self, value, cycle=""):
    id = self.build_id('timing')
    result = { '_type': 'Timing', 'timingId': id, 'type': "anchor", 'value': value, 'cycle': cycle, 'relativeToFrom': None, 'window': None, 'relativeTo': None }
    self.dicts[id] = result
    return result

  def add_condition_timing(self, value, to_id):
    id = self.build_id('timing')
    result = { '_type': 'Condition', 'conditionId': id, 'type': "condition", 'value': value, 'relativeToFrom': None, 'window': None, 'relativeTo': to_id }
    self.dicts[id] = result
    return result

  def add_cycle_start_timing(self, value):
    id = self.build_id('timing')
    result = { '_type': 'CycleStart', 'cycleStartId': id, 'type': "cycle start", 'value': value, 'relativeToFrom': None, 'window': None, 'relativeTo': None }
    self.dicts[id] = result
    return result

  def add_timeline(self, entry, timepoints, exit):
    id = self.build_id('timeline')
    result = { '_type': 'Timeline', 'timelineId': id, 'timelineEntry': entry, 'timelineTimepoints': timepoints, 'timelineExit': exit }
    self.dicts['id'] = result
    return result
  
  def add_activity(self, name, description, conditional=False, conditional_reason="", surrogates=[]):
    id = self.build_id('activity')
    result = { '_type': 'Activity', 'activityId': id, 'activityName': name, 'activityDescription': description, 'activityIsConditional': conditional, 'activityConditionalReason': conditional_reason, 'bcSurrogateIds': surrogates }
    self.dicts['id'] = result
    return result

  def add_encounter(self, name, description, enc_type, env_setting, contact_modes):
    id = self.build_id('encounter')
    result = { '_type': 'Encounter', 'encounterId': id, 'encounterName': name, 'encounterDescription': description, 'encounterType': enc_type, 'encounterEnvironmentalSetting': env_setting, 'encounterContactMode': contact_modes }
    self.dicts['id'] = result
    return result

  def add_biomedical_concept_surrogate(self, name, description, reference):
    id = self.build_id('bc_surrogate')
    result = { '_type': 'BCSurrogate', 'bcSurrogateId': id, 'bcSurrogateName': name, 'bcSurrogateDescription': description, 'bcSurrogateReference': reference }
    self.dicts['id'] = result
    return result

  def add_study_design(self, intent_types, trial_types, intervention_model, rationale, blinding, therapeutic_areas, cells):
    id = self.build_id('study_design')
    result = { '_type': 'StudyDesign', 'studyDesignId': id, 
      'studyDesignName': "Study Design",
      'studyDesignDescription': "The design for the study",
      'trialIntentTypes': intent_types,
      'trialType': trial_types,
      'interventionModel': intervention_model,
      'studyCells': cells,
      'studyIndications': [],
      'studyInvestigationalInterventions': [],
      'studyStudyDesignPopulations': [],
      'studyObjectives': [],
      'studyScheduleTimelines': [],
      'therapeuticAreas': therapeutic_areas,
      'studyEstimands': [],
      'encounters': [],
      'activities': [],
      'studyDesignRationale': rationale,
      'studyDesignBlindingScheme': blinding,
      'biomedicalConcepts': [],
      'bcCategories': [],
      'bcSurrogates': []
    }
    self.dicts['id'] = result
    return result
    
  def add_study_design_timelines(self, study_design, timelines):
    study_design['studyWorkflows'] = timelines
    return study_design

  def add_study(self, title, version, type, phase, ta, rationale, acronym, identifiers, protocols, designs):
    id = self.build_id('study')
    result = { '_type': 'Study', 'studyId': id, 'studyTitle': title, 'studyVersion': version, 'studyType': type, 'studyPhase': phase, 'businessTherapueticAreas': ta, 'studyRationale': rationale, 'studyAcronym': acronym, 'studyIdentifiers': identifiers, 'studyProtocolVersions': protocols, 'studyDesigns': designs }
    self.dicts['id'] = result
    return result
