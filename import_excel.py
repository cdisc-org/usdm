from usdm_excel.usdm_excel import USDMExcel
import os
import json

def save_as_file(raw_json, filename):
  with open('source_data/%s.json' % (filename), 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    f.write(json.dumps(json_object, indent=2))

#study = "Roche Phase 3 NCT04320615"
study = "cycles_1_v2"
#study = "simple_1"
#study = "simple_2"

program_path = os.path.abspath("import_excel.py")
file_path = os.path.join(os.path.dirname(program_path), "source_data/%s.xlsx" % (study))
x = USDMExcel(file_path)
save_as_file(x.to_json(), study)

#nodes, edges = x.to_nodes_and_edges()
#print("JSON:", json)
#print("NODES:", nodes)
#print("EDGES:", edges)