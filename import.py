from usdm_excel.usdm_excel import USDMExcel
import os
import json
import yaml

def save_as_json_file(raw_json, filename):
  with open('source_data/%s.json' % (filename), 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    f.write(json.dumps(json_object, indent=2))

def save_as_yaml_file(data, filepath):
  with open(filepath, 'w') as f:
    yaml.dump(data, f, default_flow_style=False)

def save_as_node_file(nodes, filename):
  save_as_yaml_file(nodes, 'source_data/%s_nodes.yaml' % (filename))

def save_as_edges_file(nodes, filename):
  save_as_yaml_file(nodes, 'source_data/%s_edges.yaml' % (filename))

studies = [
  #'Roche Phase 3 NCT04320615',
  #'cycles_1',
  #'simple_1',
  #'simple_2',
  'profile_1'
]

program_path = os.path.abspath("import_excel.py")
for study in studies:
  print ("Processing study %s ..." % (study))
  file_path = os.path.join(os.path.dirname(program_path), "source_data/%s.xlsx" % (study))
  usdm = USDMExcel(file_path)
  save_as_json_file(usdm.to_json(), study)
  nodes, edges = usdm.to_nodes_and_edges()
  save_as_node_file(nodes, study)
  save_as_edges_file(edges, study)