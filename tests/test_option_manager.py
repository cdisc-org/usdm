from src.usdm_excel.option_manager import *

def test_create():
  object = OptionManager()
  assert len(object.items.keys()) == 0
  assert object.items == {}

def test_set():
  option_manager.items = {}
  option_manager.set('fred', 'value')
  assert len(option_manager.items.keys()) == 1
  assert option_manager.items['fred'] == 'value'

def test_get():
  option_manager.items = {}
  option_manager.items['fred'] = 'value'
  assert option_manager.get('fred') == 'value'

def test_clear():
  option_manager.items = {}
  option_manager.items['fred'] = 'value'
  assert len(option_manager.items.keys()) == 1
  option_manager.clear()
  assert len(option_manager.items.keys()) == 0

def test_options():
  option_manager.set(Options.PREVIOUS_NEXT, PrevNextOption.NONE)
  assert option_manager.get(Options.PREVIOUS_NEXT) == PrevNextOption.NONE.value
  option_manager.set(Options.ROOT, RootOption.API_COMPLIANT)
  assert option_manager.get(Options.ROOT) == RootOption.API_COMPLIANT.value
  option_manager.set(Options.DESCRIPTION, 'Some text')
  assert option_manager.get(Options.DESCRIPTION) == 'Some text'