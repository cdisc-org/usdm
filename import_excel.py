from usdm_excel.usdm_excel import USDMExcel
import os
import json

def save_as_file(raw_json, filename):
  with open('source_data/%s.json' % (filename), 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    f.write(json.dumps(json_object, indent=2))

studies = [
  "Roche Phase 3 NCT04320615",
  "cycles_1",
  "simple_1",
  "simple_2"
]

program_path = os.path.abspath("import_excel.py")
for study in studies:
  print ("Processing study %s ..." % (study))
  file_path = os.path.join(os.path.dirname(program_path), "source_data/%s.xlsx" % (study))
  x = USDMExcel(file_path)
  save_as_file(x.to_json(), study)