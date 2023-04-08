from src.usdm_excel.errors.errors import Errors

def test_create():
  errors = Errors()
  assert errors.items == []

def test_add():
  errors = Errors()
  assert len(errors.items) == 0
  errors.add(sheet="My Sheet", row=1, column=99, message="XXXXX")
  assert len(errors.items) == 1
  assert errors.items[0].message == "XXXXX"
    
def test_count():
  errors = Errors()
  errors.add(sheet="My Sheet", row=1, column=99, message="XXXXX")
  errors.add(sheet="My Sheet", row=1, column=99, message="XXXXX")
  assert errors.count() == 2

def test_clear():
  errors = Errors()
  assert len(errors.items) == 0
  errors.add(sheet="My Sheet", row=1, column=99, message="XXXXX")
  assert len(errors.items) == 1
  errors.clear()
  assert len(errors.items) == 0

def test_dumo():
  errors = Errors()
  errors.add(sheet="My Sheet", row=1, column=99, message="XXXXX1")
  errors.add(sheet="My Sheet", row=2, column=100, message="XXXXX2")
  assert (errors.dump()) == [
    {'sheet': 'My Sheet', 'row': 1, 'column': 99, 'message': 'XXXXX1', 'level': 40},
    {'sheet': 'My Sheet', 'row': 2, 'column': 100, 'message': 'XXXXX2', 'level': 40}
  ]
