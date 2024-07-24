from usdm_excel.template_manager import *

def test_create(globals):
  object = TemplateManager(globals)
  assert len(object._items.keys()) == 0
  assert object._items == {}

def test_add(globals):
  globals.template_manager._items = {}
  globals.template_manager.add('fred', 'value')
  assert len(globals.template_manager._items.keys()) == 1
  assert globals.template_manager._items['FRED'] == 'value'
  globals.template_manager.add('Sid1', 'value')
  assert len(globals.template_manager._items.keys()) == 2
  assert globals.template_manager._items['SID1'] == 'value'

def test_all(globals):
  globals.template_manager._items = {'FRED': 'value1', 'SID1': 'value2'}
  assert len(globals.template_manager._items.keys()) == 2
  assert globals.template_manager.all() == ['value1', 'value2']

def test_get(globals):
  globals.template_manager._items = {}
  globals.template_manager._items['FRED'] = 'value'
  assert globals.template_manager.get('fred') == 'value'
  assert globals.template_manager.get('FRED') == 'value'

def test_clear(globals):
  globals.template_manager._items = {}
  globals.template_manager._items['fred'] = 'value'
  assert len(globals.template_manager._items.keys()) == 1
  globals.template_manager.clear()
  assert len(globals.template_manager._items.keys()) == 0
