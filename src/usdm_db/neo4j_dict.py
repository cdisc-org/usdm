import json
import stringcase
from uuid import uuid4


class Neo4jDict:
    class LogicError(Exception):
        pass

    def __init__(self, study):
        self.study = study
        self.nodes = {}
        self.edges = {}
        self.add_edges = []
        self.node_id_to_uuid_map = {}

    def to_dict(self):
        node = json.loads(self.study.to_json_with_type())
        self._process_node(node)
        for edge in self.add_edges:
            if edge["end"] in self.node_id_to_uuid_map:
                self._add_edge(
                    edge["start"],
                    self.node_id_to_uuid_map[edge["end"]],
                    edge["raw_relation"],
                )
            else:
                raise self.LogicError(
                    f"{edge['start']} --edge-> {edge['end']} [{edge}]"
                )
        return {"nodes": self.nodes, "edges": self.edges}

    def _process_node(self, node):
        if type(node) == list:
            if node:
                return [self._process_node(item) for item in node]
            else:
                return None
        elif type(node) == dict and "_type" not in node:
            return str(node)
        elif type(node) == dict:
            properties = {}
            this_node_uuid = str(uuid4())
            for key, value in node.items():
                if self._is_edge_field(key):
                    self._edge_field(key, value, this_node_uuid)
                else:
                    result = self._process_node(value)
                    if result == None:
                        pass
                    elif isinstance(result, list):
                        if isinstance(result[0], str):
                            properties[key] = value
                        else:
                            for item in result:
                                self._add_edge(this_node_uuid, item["uuid"], key)
                    elif isinstance(result, dict):
                        self._add_edge(this_node_uuid, result["uuid"], key)
                    else:
                        properties[key] = value
            self._add_node(node["_type"], this_node_uuid, properties)
            self.node_id_to_uuid_map[properties["id"]] = this_node_uuid
            return properties
        else:
            return node

    def _add_node(self, klass, uuid, properties):
        if klass == "Study":
            properties["id"] = uuid
            # print(f"Properties: {properties}")
        if klass not in self.nodes:
            self.nodes[klass] = []
        properties.pop("_type")
        properties["uuid"] = uuid
        self.nodes[klass].append(properties)

    def _is_edge_field(self, key):
        if key == "conditionAssignments" or key.endswith("Ids") or key.endswith("Id"):
            return True
        return False

    def _edge_field(self, key, value, current_index):
        # if key == "conditionAssignments":
        #   for item in value:
        #     self._add_post_edge(current_index, item['conditionTargetId'], key)
        # elif key.endswith('Ids'):
        if key.endswith("Ids"):
            for item in value:
                if item:
                    self._add_post_edge(current_index, item, key)
        elif key.endswith("Id"):
            if value:
                self._add_post_edge(current_index, value, key)

    def _add_post_edge(self, start, end, key):
        self.add_edges.append({"start": start, "end": end, "raw_relation": key})

    def _add_edge(self, start, end, key):
        rel = self._rel_name(key)
        name = f"{stringcase.snakecase(rel).upper()}_REL"
        if name not in self.edges:
            self.edges[name] = []
        self.edges[name].append({"start": start, "end": end})

    def _rel_name(self, key):
        if key == "conditionAssignments":
            return key
        elif key.endswith("Ids"):
            return key[:-3]
        elif key.endswith("Id"):
            return key[:-2]
        return key
