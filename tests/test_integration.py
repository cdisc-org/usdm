import json
import csv
from src.usdm_excel import USDMExcel

SAVE_ALL = False

def save_error_csv(file, contents):
  writer = csv.DictWriter(file, fieldnames=['sheet','row','column','message','level'])
  writer.writeheader()
  writer.writerows(contents)

def read_error_csv(file):
  reader = csv.DictReader(file)
  items = list(reader)
  for item in items:
    item['row'] = int(item['row'])
    item['column'] = int(item['column'])
  return items

def run_test(filename, save=False):
  print(f"RUN: S={save}")
  excel = USDMExcel(f"tests/integration_test_files/{filename}.xlsx")
  result = excel.to_json()
  errors = excel.errors()

  # Useful if you want to see the results.
  print(f"ERRORS: S={save} E={errors}")
  if save or SAVE_ALL:
    with open(f"tests/integration_test_files/{filename}.json", 'w', encoding='utf-8') as f:
      f.write(json.dumps(json.loads(result), indent=2))
    print(f"ERRORS: {errors}")
    with open(f"tests/integration_test_files/{filename}_errors.csv", 'w',newline='') as f:
      save_error_csv(f, errors) 
  
  with open(f"tests/integration_test_files/{filename}.json", 'r') as f:
    expected = json.dumps(json.load(f)) # Odd, but doing it for consistency of processing
  assert result == expected
  with open(f"tests/integration_test_files/{filename}_errors.csv", 'r') as f:
    expected = read_error_csv(f)
  assert errors == expected

def run_test_ne(filename, save=False):
  result = {}
  excel = USDMExcel(f"tests/integration_test_files/{filename}.xlsx")
  result['n'], result['e'] = excel.to_nodes_and_edges()
  for type in ['n', 'e']:

    # Useful if you want to see the results.
    if save or SAVE_ALL:
      with open(f"tests/integration_test_files/{filename}_{type}.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(result[type], indent=2))
    
    with open(f"tests/integration_test_files/{filename}_{type}.json", 'r') as f:
      expected = json.load(f)
    assert result[type] == expected

def test_simple_1():
  run_test('simple_1')

def test_simple_1_ne():
  run_test_ne('simple_1')

def test_config_1():
  run_test('config_1')

def test_config_2():
  run_test('config_2')

def test_no_activity_sheet():
  run_test('no_activity_sheet')

def test_address_comma():
  run_test('address')

def test_complex_1():
  run_test('complex_1')

def test_complex_1_ne():
  run_test_ne('complex_1')

def test_arms_epochs_1():
  run_test('arms_epochs')

def test_arms_epochs_1_ne():
  run_test_ne('arms_epochs')
