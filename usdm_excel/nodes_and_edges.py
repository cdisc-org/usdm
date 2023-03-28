import stringcase
import json

class NodesAndEdges():

  def __init__(self, study):
    self.study = study
    self.nodes = []
    self.edges = []
    self.add_edges = []
    self.node_index = 1
    self.edge_index = 1
    self.id_node_index_map = {}
    self.edge_attributes = [
      'encounterIds',
      'timepointActivityIds',
      'timepointEncounterId',
      'bcSurrogateIds',
      'bcCategoryIds',
      'biomedicalConceptIds',
      'biomedicalConceptSurrogateId',
      'relativeFromScheduledInstanceId',
      'relativeToScheduledInstanceId',
      'scheduledInstanceEncounterId',
      'activityIds',
      'scheduledDecisionInstanceId',
      'treatment',
      'variableOfInterest',
      'conditionAssignments',
      'activityTimelineId'
    ]
    self.fix_id_name = {
      'scheduledActivityInstanceId': 'scheduledInstanceId',
      'scheduledDecisionInstanceId': 'scheduledInstanceId',
      'biomedicalConceptSurrogateId': 'bcSurrogateId',
      'biomedicalConceptPropertyId': 'bcPropertyId'
    }
  
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
        result = result + indexes
      return result
    elif type(node) == dict:
      if node == {}:
        return []
      properties = {}
      id_field, klass = self._get_id_field_and_klass(node)
      if node[id_field] in self.id_node_index_map:
        return [self.id_node_index_map[node[id_field]]]
      this_node_index = self.node_index
      self.node_index += 1
      for key, value in node.items():
        if key in self.edge_attributes:
          if key == "conditionAssignments":
            # Special case, array of arrays of condition and link id
            for item in value:
              self.add_edges.append( { 'start': this_node_index, 'end': item[1], 'properties': { 'label': key, 'type': 'Condition' }})
          elif type(value) == list:
            for item in value:
              self.add_edges.append( { 'start': this_node_index, 'end': item, 'properties': { 'label': key, 'type': 'List' }})
          else:
            if not value == "":
              self.add_edges.append( { 'start': this_node_index, 'end': value, 'properties': { 'label': key, 'type': 'Other' }})
            # else:
            #   print("Key %s, value >%s<" % (key, value))
        else:
          indexes = self._process_node(value)
          if indexes == []:
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

