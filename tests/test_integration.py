import json
from src.usdm_excel import USDMExcel

def run_test(filename):
  excel = USDMExcel(f"tests/integration_test_files/{filename}.xlsx")
  with open(f"tests/integration_test_files/{filename}.json", 'r') as f:
    expected = json.dumps(json.load(f)) # Odd, but doing it for consistency of processing
  result = excel.to_json()
  # Useful if you want to see the results
  with open(f"tests/integration_test_files/{filename}_result.json", 'w', encoding='utf-8') as f:
    f.write(json.dumps(json.loads(excel.to_json()), indent=2))
  assert result == expected

def test_simple_1():
  run_test('simple_1')

def test_config_1():
  run_test('config_1')
