from usdm_excel.template_manager import *

def test_create(globals):
  object = TemplateManager(globals)
  assert len(object._items.keys()) == 1
  assert object._items == {'SPONSOR': 'document'}

def test_default(globals):
  object = TemplateManager(globals)
  assert object.default_template == 'SPONSOR'

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

def test_tidy_remove_default_1(globals):
  object = TemplateManager(globals)
  object.add('fred', 'value_fred')
  object.add('Sid', 'value_sid')
  object.tidy(['value_fred', 'value_sid'])
  assert len(object._items.keys()) == 2
  assert object._items['FRED'] == 'value_fred'
  assert object._items['SID'] == 'value_sid'

def test_tidy_remove_default_2(globals):
  object = TemplateManager(globals)
  object.add('fred', 'value_fred')
  object.add('Sid', 'value_sid')
  object.tidy(['value_fred', 'value_sid', 'document'])
  assert len(object._items.keys()) == 3
  assert object._items['FRED'] == 'value_fred'
  assert object._items['SID'] == 'value_sid'
  assert object._items['SPONSOR'] == 'document'
