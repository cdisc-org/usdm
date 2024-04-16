from usdm_db.errors_and_logging.errors import Errors
from usdm_db.errors_and_logging.error import Error

def test_create():
  error = Errors()
  assert error.items == []

def test_clear():
  error = Errors()
  error.items = ['item 1', 'item 2']
  assert len(error.items) == 2
  error.clear()
  assert len(error.items) == 0
  assert error.items == []
  
def test_count():
  error = Errors()
  error.items = ['item 1', 'item 2']
  assert error.count() == 2

def test_add():
  error = Errors()
  error.add(message='a message')
  assert len(error.items) == 1
  assert error.items[0].to_dict() == {'level': 'Error', 'message': 'a message'}

def test_dump():
  error = Errors()
  error.items.append(Error(message="Test message 1"))
  error.items.append(Error(message="Test message 2", level=Error.WARNING))
  assert error.dump(Errors.DEBUG) == [
    {'level': 'Error', 'message': 'Test message 1'},
    {'level': 'Warning', 'message': 'Test message 2'},
  ]
