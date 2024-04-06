from usdm_excel.option_manager import *
from tests.test_factory import Factory

factory = Factory()
globals = factory.globals

def test_create():
  object = OptionManager(globals)
  assert len(object._items.keys()) == 0
  assert object._items == {}

def test_set():
  globals.option_manager._items = {}
  globals.option_manager.set('fred', 'value')
  assert len(globals.option_manager._items.keys()) == 1
  assert globals.option_manager._items['fred'] == 'value'

def test_get():
  globals.option_manager._items = {}
  globals.option_manager._items['fred'] = 'value'
  assert globals.option_manager.get('fred') == 'value'

def test_clear():
  globals.option_manager._items = {}
  globals.option_manager._items['fred'] = 'value'
  assert len(globals.option_manager._items.keys()) == 1
  globals.option_manager.clear()
  assert len(globals.option_manager._items.keys()) == 0

def test_options():
  globals.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.NONE)
  assert globals.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.NONE.value
  globals.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.EMPTY)
  assert globals.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value
  globals.option_manager.set(Options.USDM_VERSION, 2)
  assert globals.option_manager.get(Options.USDM_VERSION) == '2'
  globals.option_manager.set(Options.USDM_VERSION, 3)
  assert globals.option_manager.get(Options.USDM_VERSION) == '3'
  # globals.option_manager.set(Options.ROOT, RootOption.API_COMPLIANT)
  # assert globals.option_manager.get(Options.ROOT) == RootOption.API_COMPLIANT.value
  # globals.option_manager.set(Options.DESCRIPTION, 'Some text')
  # assert globals.option_manager.get(Options.DESCRIPTION) == 'Some text'