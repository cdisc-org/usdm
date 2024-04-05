from usdm_excel.option_manager import *

def test_create():
  object = OptionManager()
  assert len(object.items.keys()) == 0
  assert object.items == {}

def test_set():
  self.managers.option_manager.items = {}
  self.managers.option_manager.set('fred', 'value')
  assert len(self.managers.option_manager.items.keys()) == 1
  assert self.managers.option_manager.items['fred'] == 'value'

def test_get():
  self.managers.option_manager.items = {}
  self.managers.option_manager.items['fred'] = 'value'
  assert self.managers.option_manager.get('fred') == 'value'

def test_clear():
  self.managers.option_manager.items = {}
  self.managers.option_manager.items['fred'] = 'value'
  assert len(self.managers.option_manager.items.keys()) == 1
  self.managers.option_manager.clear()
  assert len(self.managers.option_manager.items.keys()) == 0

def test_options():
  self.managers.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.NONE)
  assert self.managers.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.NONE.value
  self.managers.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.EMPTY)
  assert self.managers.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value
  self.managers.option_manager.set(Options.USDM_VERSION, 2)
  assert self.managers.option_manager.get(Options.USDM_VERSION) == '2'
  self.managers.option_manager.set(Options.USDM_VERSION, 3)
  assert self.managers.option_manager.get(Options.USDM_VERSION) == '3'
  # self.managers.option_manager.set(Options.ROOT, RootOption.API_COMPLIANT)
  # assert self.managers.option_manager.get(Options.ROOT) == RootOption.API_COMPLIANT.value
  # self.managers.option_manager.set(Options.DESCRIPTION, 'Some text')
  # assert self.managers.option_manager.get(Options.DESCRIPTION) == 'Some text'