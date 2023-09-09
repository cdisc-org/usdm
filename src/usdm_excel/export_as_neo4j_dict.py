import json

class ExportAsNeo4jDict():

  def __init__(self, study):
    self.study = study
    self.nodes = []
    self.edges = []
    self.add_edges = []
    self.node_index = 1
    self.edge_index = 1
    self.id_node_index_map = {}
      
  def export(self):
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
    return {'nodes': self.nodes, 'edges': self.edges}
  
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
      klass = node['_type']
      if node['id'] in self.id_node_index_map:
        return [self.id_node_index_map[node['id']]]
      this_node_index = self.node_index
      self.node_index += 1
      for key, value in node.items():
        if self._is_edge_field(key):
          self._edge_field(key, value, this_node_index)
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
        properties['id'] = "Study"
      self.nodes.append({ 'id': this_node_index, 'properties': properties })
      self.id_node_index_map[properties['id']] = this_node_index
      return [this_node_index]
    else:
      return []
    
  def _is_edge_field(self, key):
    if key == "conditionAssignments" or key.endswith('Ids') or key.endswith('Id'):
      return True
    return False

  def _edge_field(self, key, value, current_index):
    if key == "conditionAssignments":
      for item in value:
        self.add_edges.append( { 'start': current_index, 'end': item[1], 'properties': { 'label': key, 'type': 'Condition' }})
    elif key.endswith('Ids'):
      for item in value:
        if item:
          self.add_edges.append( { 'start': current_index, 'end': item, 'properties': { 'label': key, 'type': 'List' }})
    elif key.endswith('Id'):
      if value:
        self.add_edges.append( { 'start': current_index, 'end': value, 'properties': { 'label': key, 'type': 'Other' }})
