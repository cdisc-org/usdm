import json

class ExportAsNeo4jDict():

  class LogicError(Exception):
    pass
  
  def __init__(self, study):
    self.study = study
    self.nodes = {}
    self.edges = {}
    self.add_edges = []
    self.node_index = 1
    self.edge_index = 1
    self.id_node_index_map = {}
      
  def export(self):
    node = json.loads(self.study.to_json_with_type())
    self._process_node(node)
    for edge in self.add_edges:
      if edge['end'] in self.id_node_index_map:
        self._add_edge(edge['start'], self.id_node_index_map[edge['end']], self.edge_index, edge['label'], edge['type'])
        self.edge_index += 1
      else:
        raise self.LogicError(f"{edge['start']} --edge-> {edge['end']} [{edge}]")
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
              self._add_edge(this_node_index, index, self.edge_index, key, 'Normal')
              self.edge_index += 1
      if klass == "Study":
        properties['id'] = "Study"   
      self._add_node(klass, properties)
      self.id_node_index_map[properties['id']] = this_node_index
      return [this_node_index]
    else:
      return []

  def _add_node(self, klass, properties):
    if klass not in self.nodes:
      self.nodes[klass] = []
    self.nodes[klass].append(properties)

  def _is_edge_field(self, key):
    if key == "conditionAssignments" or key.endswith('Ids') or key.endswith('Id'):
      return True
    return False

  def _edge_field(self, key, value, current_index):
    if key == "conditionAssignments":
      for item in value:
        self._add_post_edge(current_index, item[1], key, 'Condition')
    elif key.endswith('Ids'):
      for item in value:
        if item:
          self._add_post_edge(current_index, item, key, 'List')
    elif key.endswith('Id'):
      if value:
        self._add_post_edge(current_index, value, key, 'Other')

  def _add_post_edge(self, start, end, key, type):
    rel = self._rel_name(key)
    self.add_edges.append({'start': start, 'end': end, 'label': key, 'relation': rel, 'type': type})

  def _add_edge(self, start, end, id, key, type):
    rel = self._rel_name(key)
    if rel not in self.edges:
      self.edges[rel] = []
    self.edges[rel].append({'id': id, 'start': start, 'end': end, 'label': key, 'relation': rel, 'type': type})

  def _rel_name(self, key):
    if key == "conditionAssignments":
      return key
    elif key.endswith('Ids'):
      return key[:-3]
    elif key.endswith('Id'):
      return key[:-2]
    return key