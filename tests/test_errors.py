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
  errors.add(sheet="My Sheet", row=3, column=101, message="XXXXX3", level=Errors.WARNING)
  errors.add(sheet="My Sheet", row=4, column=102, message="XXXXX4", level=Errors.INFO)
  errors.add(sheet="My Sheet", row=5, column=103, message="XXXXX5", level=Errors.DEBUG)
  assert (errors.dump(Errors.DEBUG)) == [
    {'sheet': 'My Sheet', 'row': 1, 'column': 99, 'message': 'XXXXX1', 'level': 'Error'},
    {'sheet': 'My Sheet', 'row': 2, 'column': 100, 'message': 'XXXXX2', 'level': 'Error'},
    {'sheet': 'My Sheet', 'row': 3, 'column': 101, 'message': 'XXXXX3', 'level': 'Warning'},
    {'sheet': 'My Sheet', 'row': 4, 'column': 102, 'message': 'XXXXX4', 'level': 'Info'},
    {'sheet': 'My Sheet', 'row': 5, 'column': 103, 'message': 'XXXXX5', 'level': 'Debug'}
  ]
  assert (errors.dump(Errors.ERROR)) == [
    {'sheet': 'My Sheet', 'row': 1, 'column': 99, 'message': 'XXXXX1', 'level': 'Error'},
    {'sheet': 'My Sheet', 'row': 2, 'column': 100, 'message': 'XXXXX2', 'level': 'Error'}
  ]
  assert (errors.dump(Errors.WARNING)) == [
    {'sheet': 'My Sheet', 'row': 1, 'column': 99, 'message': 'XXXXX1', 'level': 'Error'},
    {'sheet': 'My Sheet', 'row': 2, 'column': 100, 'message': 'XXXXX2', 'level': 'Error'},
    {'sheet': 'My Sheet', 'row': 3, 'column': 101, 'message': 'XXXXX3', 'level': 'Warning'}
  ]
