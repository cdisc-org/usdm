from usdm_excel.cdisc_biomedical_concept import CDISCBiomedicalConcepts
import os
import json
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.id_manager import IdManager

def save_as_file(raw_json, filename):
  with open('source_data/%s.json' % (filename), 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    f.write(json.dumps(json_object, indent=2))

id_manager = IdManager()
bc = CDISCBiomedicalConcepts(id_manager)
print("Weight:", bc.usdm("Body Weight"))
