import yaml
import csv
from src.usdm_excel import USDMExcel
from uuid import UUID

SAVE_ALL = False

def to_int(value):
  try:
    return int(value)
  except:
    return None

def read_error_csv(file):
  reader = csv.DictReader(file)
  items = list(reader)
  for item in items:
    item['row'] = to_int(item['row'])
    item['column'] = to_int(item['column'])
  return items

def run_test(filename, save=False):
  excel = USDMExcel(f"tests/integration_test_files/{filename}.xlsx")
  result = excel.to_neo4j_dict()

  # Useful if you want to see the results.
  if save or SAVE_ALL:
    with open(f"tests/integration_test_files/{filename}_neo4j_dict.yaml", 'w') as f:
      f.write(yaml.dump(result))
  
  with open(f"tests/integration_test_files/{filename}_neo4j_dict.yaml", 'r') as f:
    expected = yaml.safe_load(f) 
  assert result == expected

def test_simple_1(mocker):
  fake_uuids = (UUID(f'00000000-0000-4000-8000-{i:012}', version=4) for i in range(10000))
  mocker.patch("usdm_excel.export_as_neo4j_dict.uuid4", side_effect=fake_uuids)
  run_test('simple_1')

