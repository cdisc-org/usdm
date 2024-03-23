import json

class ExportAsYworksDict():

  FULL = "full"
  TIMELINE = "timeline"

  def __init__(self, study, view=FULL):
    self.study = study
    self.nodes = []
    self.edges = []
    self.add_edges = []
    self.node_index = 1
    self.edge_index = 1
    self.id_node_index_map = {}
    # self.edge_attributes = {
    #   'ScheduledActivityInstance': [
    #     'activityIds',
    #     'encounterId',
    #     'epochId',
    #     'defaultConditionId',
    #   ],
    #   'ScheduledDecisionInstance': [
    #     'activityIds',
    #     'epochId',
    #     'defaultConditionId'
    #   ],
    #   'ConditionAssignment': [
    #     'conditionTargetId'
    #   ],
    #   'Activity': [
    #     'bcSurrogateIds',
    #     'bcCategoryIds',
    #     'biomedicalConceptIds',
    #   ],
    #   'Timing': [
    #     'relativeFromScheduledInstanceId',
    #     'relativeToScheduledInstanceId',
    #   ],
    #   'Estimand': [
    #     'interventionId',
    #     'variableOfInterestId'
    #   ],
    #   'ScheduledTimeline': [
    #     'activityTimelineId',
    #   ],
    #   'StudyCell': [
    #     'studyArmId',
    #     'studyEpochId',
    #     'studyElementIds',
    #   ]
    # }
    self.order_attributes = []
    self.ignore_klass = []
    self.collapse_klass = []
    if view == self.__class__.TIMELINE:
      self.ignore_klass = [
        'StudyProtocolVersion', 'StudyIdentifier', 'Indication', 
        'InvestigationalIntervention', 'Objective', 'StudyDesignPopulation', 
        'Estimand', 'StudyCell', 'TransitionRule', 'StudyArm', 'StudyEpoch', 'StudyElement',
        'BiomedicalConcept', 'BiomedicalConceptCategory', 'BiomedicalConceptSurrogate', 
        'Procedure', 'AliasCode', 'NarrativeContent', 'StudyAmendment', 'EligibilityCriteria', 
        'StudyProtocolDocument', 'GovernanceDate'
      ]
      self.collapse_klass = ['Code']
      
  def export(self):
    node = json.loads(self.study.to_json_with_type())
    #print(f"NODE: {node}")
    self._process_node(node)
    for edge in self.add_edges:
      #print(f"EDGE: {edge}")
      if edge['end'] in self.id_node_index_map:
        edge['id'] = self.edge_index
        edge['end'] = self.id_node_index_map[edge['end']]
        self.edges.append(edge)
        self.edge_index += 1
      else:
        node_details = next((i for i in self.nodes if i["id"] == edge['start']), None)
        node_id = node_details['properties']['id']
        node_type = node_details['properties']['_type']
        print("***** %s [%s, %s] -- edge -> %s [%s] *****" % (edge['start'], node_type, node_id, edge['end'], edge['properties']))
    return self.nodes, self.edges
  
  def _process_node(self, node):
    if type(node) == list:
      result = []
      for item in node:
        indexes = self._process_node(item)
        if indexes is None:
          return None
        result = result + indexes
      return result
    elif type(node) == dict:
      if node == {}:
        return []
      properties = {}
      id_field, klass = self._get_id_field_and_klass(node)
      if not klass:
        return None
      if klass in self.ignore_klass:
        return None
      if node[id_field] in self.id_node_index_map:
        return [self.id_node_index_map[node[id_field]]]
      this_node_index = self.node_index
      self.node_index += 1
      if klass in self.collapse_klass:
        return []
      for key, value in node.items():
        if key.endswith('Id') or key.endswith('Ids'):
        #if klass in self.edge_attributes and key in self.edge_attributes[klass]:
          # if key == "conditionAssignments":
          #   # Special case, array of arrays of condition and link id
          #   for item in value:
          #     self.add_edges.append( { 'start': this_node_index, 'end': item[1], 'properties': { 'label': key, 'type': 'Condition' }})
          # # elif key == "parameterMap":
          # #   properties[key] = value
          # elif type(value) == list:
          if type(value) == list:
            for item in value:
              if item:
                self.add_edges.append( { 'start': this_node_index, 'end': item, 'properties': { 'label': key, 'type': 'List' }})
          else:
            if value:
              self.add_edges.append( { 'start': this_node_index, 'end': value, 'properties': { 'label': key, 'type': 'Other' }})
        else:
          indexes = self._process_node(value)
          if indexes == None:
            properties[key] = {}
          elif indexes == []:
            properties[key] = value
          else:
            for index in indexes:
              self.edges.append( {'id': self.edge_index, 'start': this_node_index, 'end': index, 'properties': {'label': key}})
              self.edge_index += 1
      if klass == "Study":
        node[id_field] = "Study"
      properties['label'] = node[id_field]
      self.nodes.append({ 'id': this_node_index, 'properties': properties })
      self.id_node_index_map[properties[id_field]] = this_node_index
      return [this_node_index]
    else:
      return []
    
  def _get_id_field_and_klass(self, node):
    try:
      klass = node['_type']
      return 'id', klass
    except Exception as e:
      return 'id', None

