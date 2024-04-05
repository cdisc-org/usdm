from usdm_excel.option_manager import *
from tests.test_factory import Factory

factory = Factory()
managers = factory.managers()

def test_create():
  object = OptionManager(managers)
  assert len(object._items.keys()) == 0
  assert object._items == {}

def test_set():
  managers.option_manager._items = {}
  managers.option_manager.set('fred', 'value')
  assert len(managers.option_manager._items.keys()) == 1
  assert managers.option_manager._items['fred'] == 'value'

def test_get():
  managers.option_manager._items = {}
  managers.option_manager._items['fred'] = 'value'
  assert managers.option_manager.get('fred') == 'value'

def test_clear():
  managers.option_manager._items = {}
  managers.option_manager._items['fred'] = 'value'
  assert len(managers.option_manager._items.keys()) == 1
  managers.option_manager.clear()
  assert len(managers.option_manager._items.keys()) == 0

def test_options():
  managers.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.NONE)
  assert managers.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.NONE.value
  managers.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.EMPTY)
  assert managers.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value
  managers.option_manager.set(Options.USDM_VERSION, 2)
  assert managers.option_manager.get(Options.USDM_VERSION) == '2'
  managers.option_manager.set(Options.USDM_VERSION, 3)
  assert managers.option_manager.get(Options.USDM_VERSION) == '3'
  # managers.option_manager.set(Options.ROOT, RootOption.API_COMPLIANT)
  # assert managers.option_manager.get(Options.ROOT) == RootOption.API_COMPLIANT.value
  # managers.option_manager.set(Options.DESCRIPTION, 'Some text')
  # assert managers.option_manager.get(Options.DESCRIPTION) == 'Some text'