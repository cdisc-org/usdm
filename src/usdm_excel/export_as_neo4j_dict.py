import stringcase
import json
from uuid import uuid4

class ExportAsNeo4jDict():

  class LogicError(Exception):
    pass
  
  def __init__(self, study):
    self.study = study
    self.nodes = {}
    self.edges = {}
    self.add_edges = []
    #self.node_index = 1
    #self.edge_index = 1
    self.node_id_to_uuid_map = {}
      
  def export(self):
    node = json.loads(self.study.to_json_with_type())
    self._process_node(node)
    for edge in self.add_edges:
      if edge['end'] in self.node_id_to_uuid_map:
        self._add_edge(edge['start'], self.node_id_to_uuid_map[edge['end']], edge['raw_relation'])
      else:
        raise self.LogicError(f"{edge['start']} --edge-> {edge['end']} [{edge}]")
    return {'nodes': self.nodes, 'edges': self.edges}
  
  def _process_node(self, node):
    if type(node) == list:
      result = []
      for item in node:
        uuids = self._process_node(item)
        if uuids is None:
          return None
        result = result + uuids
      return result
    elif type(node) == dict:
      if node == {}:
        return []
      properties = {}
      klass = node['_type']
      if node['id'] in self.node_id_to_uuid_map:
        return [self.node_id_to_uuid_map[node['id']]]
      this_node_uuid = str(uuid4())
      for key, value in node.items():
        if self._is_edge_field(key):
          self._edge_field(key, value, this_node_uuid)
        else:
          uuids = self._process_node(value)
          if uuids == None:
            properties[key] = {}
          elif uuids == []:
            properties[key] = value
          else:
            for uuid in uuids:
              self._add_edge(this_node_uuid, uuid, key)
      if klass == "Study":
        properties['id'] = this_node_uuid 
      self._add_node(klass, this_node_uuid, properties)
      self.node_id_to_uuid_map[properties['id']] = this_node_uuid
      return [this_node_uuid]
    else:
      return []

  def _add_node(self, klass, uuid, properties):
    if klass not in self.nodes:
      self.nodes[klass] = []
    properties.pop('_type')
    properties['uuid'] = uuid
    self.nodes[klass].append(properties)

  def _is_edge_field(self, key):
    if key == "conditionAssignments" or key.endswith('Ids') or key.endswith('Id'):
      return True
    return False

  def _edge_field(self, key, value, current_index):
    if key == "conditionAssignments":
      for item in value:
        self._add_post_edge(current_index, item[1], key)
    elif key.endswith('Ids'):
      for item in value:
        if item:
          self._add_post_edge(current_index, item, key)
    elif key.endswith('Id'):
      if value:
        self._add_post_edge(current_index, value, key)

  def _add_post_edge(self, start, end, key):
    self.add_edges.append({'start': start, 'end': end, 'raw_relation': key})

  def _add_edge(self, start, end, key):
    rel = self._rel_name(key)
    name = stringcase.snakecase(rel).upper()
    if name not in self.edges:
      self.edges[name] = []
    self.edges[name].append({'start': start, 'end': end})

  def _rel_name(self, key):
    if key == "conditionAssignments":
      return key
    elif key.endswith('Ids'):
      return key[:-3]
    elif key.endswith('Id'):
      return key[:-2]
    return key