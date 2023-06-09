import stringcase
import json

class NodesAndEdges():

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
    self.edge_attributes = {
      'ScheduledActivityInstance': [
        'timepointActivityIds',
        'scheduledActivityInstanceEncounterId',
        'activityIds',
        'epochId',
        'defaultConditionId',
      ],
      'ScheduledDecisionInstance': [
        'timepointActivityIds',
        'epochId',
        'defaultConditionId',
        'conditionAssignments',
      ],
      'Activity': [
        'bcSurrogateIds',
        'bcCategoryIds',
        'biomedicalConceptIds',
      ],
      'Timing': [
        'relativeFromScheduledInstanceId',
        'relativeToScheduledInstanceId',
      ],
      'Estimand': [
        'treatment',
        'variableOfInterest',
      ],
      'ScheduledTimeline': [
        'activityTimelineId',
      ],
      'StudyCell': [
        'studyArmId',
        'studyEpochId',
        'studyElementIds',
      ]
    }
    self.fix_id_name = {
      'scheduledActivityInstanceId': 'scheduledInstanceId',
      'scheduledDecisionInstanceId': 'scheduledInstanceId',
      'biomedicalConceptSurrogateId': 'bcSurrogateId',
      'biomedicalConceptPropertyId': 'bcPropertyId'
    }
    self.order_attributes = []
    self.ignore_klass = []
    self.collapse_klass = []
    if view == self.__class__.TIMELINE:
      self.ignore_klass = [
        'StudyProtocolVersion', 'StudyIdentifier', 'Indication', 
        'InvestigationalIntervention', 'Objective', 'StudyDesignPopulation', 
        'Estimand', 'StudyCell', 'TransitionRule', 'StudyArm', 'StudyEpoch', 'StudyElement',
        'BiomedicalConcept', 'BiomedicalConceptCategory', 'BiomedicalConceptSurrogate', 
        'Procedure', 'AliasCode'
      ]
      self.collapse_klass = ['Code']
      #self.order_attributes = [
      #  'scheduleSequenceNumber'
      #]
    #self.sequence_number_map = {}
      
  def nodes_and_edges(self):
    node = json.loads(self.study.to_json_with_type())
    self._process_node(node)
    for edge in self.add_edges:
      if edge['end'] in self.id_node_index_map:
        edge['id'] = self.edge_index
        edge['end'] = self.id_node_index_map[edge['end']]
        self.edges.append(edge)
        self.edge_index += 1
      else:
        print("***** %s -edge-> %s [%s] *****" % (edge['start'], edge['end'], edge['properties']))
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
      if klass in self.ignore_klass:
        return None
      if node[id_field] in self.id_node_index_map:
        return [self.id_node_index_map[node[id_field]]]
      this_node_index = self.node_index
      self.node_index += 1
      if klass in self.collapse_klass:
        return []
      for key, value in node.items():
        # Special case, get the ids for the sequence numbers but within scope of each timeline
        # if key == "scheduleTimelineInstances":
        #   self.sequence_number_map = {}
        #   for item in value:
        #     self.sequence_number_map[item['scheduleSequenceNumber']] = item['scheduledInstanceId']
        # Link the sequence numbers
        # if key in self.order_attributes:
        #   seq = value + 1
        #   if seq in self.sequence_number_map:
        #     self.add_edges.append( { 'start': this_node_index, 'end': self.sequence_number_map[seq], 'properties': { 'label': key, 'type': 'Order' }})
        if klass in self.edge_attributes and key in self.edge_attributes[klass]:
          if key == "conditionAssignments":
            # Special case, array of arrays of condition and link id
            for item in value:
              self.add_edges.append( { 'start': this_node_index, 'end': item[1], 'properties': { 'label': key, 'type': 'Condition' }})
          elif type(value) == list:
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
    klass = node['_type']
    id_name = "%s%s" % (stringcase.camelcase(klass), "Id")
    if id_name in self.fix_id_name:
      id_name = self.fix_id_name[id_name]
    return id_name, klass

