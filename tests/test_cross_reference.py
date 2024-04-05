import pytest
from usdm_excel.cross_ref import *

class CRTest():

  def __init__(self, id, name):
    self.id = id
    self.name = name
    self.value = "VALUE"

class CRTest2():

  def __init__(self, id, name, instance):
    self.id = id
    self.name = name
    self.child = instance
    self.value = "VALUE"

class CRTest3():

  def __init__(self, id, name, instance):
    self.id = id
    self.name = name
    self.child = instance
    self.value = "VALUE"

def test_create():
  object = CrossRef()
  assert len(object.references.keys()) == 0
  assert object.references == {}

def test_clear():
  item = CRTest(id="1234", name="name")
  self.managers.cross_references.references = {}
  self.managers.cross_references.identifiers = {}
  self.managers.cross_references.references["CRTest.name"] = item
  self.managers.cross_references.identifiers["CRTest.1234"] = item
  assert len(self.managers.cross_references.references.keys()) == 1
  assert len(self.managers.cross_references.identifiers.keys()) == 1
  self.managers.cross_references.clear()
  assert len(self.managers.cross_references.references.keys()) == 0
  assert len(self.managers.cross_references.identifiers.keys()) == 0

def test_add():
  item = CRTest(id="1234", name="name")
  self.managers.cross_references.clear()
  assert len(self.managers.cross_references.references.keys()) == 0
  assert len(self.managers.cross_references.identifiers.keys()) == 0
  self.managers.cross_references.add("name", item)
  assert len(self.managers.cross_references.references.keys()) == 1
  assert self.managers.cross_references.references["CRTest.name"] == item
  assert len(self.managers.cross_references.identifiers.keys()) == 1
  assert self.managers.cross_references.identifiers["CRTest.1234"] == item

def test_get():
  item = CRTest(id="1234", name="name")
  self.managers.cross_references.clear()
  assert len(self.managers.cross_references.references.keys()) == 0
  assert len(self.managers.cross_references.identifiers.keys()) == 0
  self.managers.cross_references.references["CRTest.name"] = item
  assert self.managers.cross_references.get(CRTest, "name") == item

def test_get_by_id():
  item = CRTest(id="1234", name="name")
  self.managers.cross_references.clear()
  assert len(self.managers.cross_references.references.keys()) == 0
  assert len(self.managers.cross_references.identifiers.keys()) == 0
  self.managers.cross_references.identifiers["CRTest.1234"] = item
  assert self.managers.cross_references.get_by_id(CRTest, "1234") == item
  assert self.managers.cross_references.get_by_id("CRTest", "1234") == item

def test_get_by_path():
  item1 = CRTest(id="1234", name="name1")
  item2 = CRTest2(id="1235", name="name2", instance=item1)
  item3 = CRTest3(id="1236", name="name3", instance=item2)
  self.managers.cross_references.clear()
  assert len(self.managers.cross_references.references.keys()) == 0
  assert len(self.managers.cross_references.identifiers.keys()) == 0
  self.managers.cross_references.add("name1", item1)
  self.managers.cross_references.add("name2", item2)  
  self.managers.cross_references.add("name3", item3)
  instance, attribute = self.managers.cross_references.get_by_path("CRTest3", "name3", "child/CRTest2/@child/CRTest/@value")
  assert instance.id == "1234"
  assert attribute == "value"
  instance, attribute = self.managers.cross_references.get_by_path("CRTest3", "name3", "child/CRTest2/child/CRTest/@value")
  assert instance.id == "1234"
  assert attribute == "value"

def test_get_by_path_errors():
  item1 = CRTest(id="1234", name="name1")
  item2 = CRTest2(id="1235", name="name2", instance=item1)
  item3 = CRTest3(id="1236", name="name3", instance=item2)
  self.managers.cross_references.clear()
  assert len(self.managers.cross_references.references.keys()) == 0
  assert len(self.managers.cross_references.identifiers.keys()) == 0
  self.managers.cross_references.add("name1", item1)
  self.managers.cross_references.add("name2", item2)  
  self.managers.cross_references.add("name3", item3)
  with pytest.raises(self.managers.cross_references.PathError) as ex_info:
    instance, attribute = self.managers.cross_references.get_by_path("CRTest4", "name3", "child/CRTest2/@child/CRTest/@value")
  assert str(ex_info.value) == "Failed to translate reference path 'child/CRTest2/@child/CRTest/@value', could not find start instance 'CRTest4', 'name3'"

  with pytest.raises(self.managers.cross_references.PathError) as ex_info:
    instance, attribute = self.managers.cross_references.get_by_path("CRTest3", "name3", "child/CRTest4/@child/CRTest/@value")
  assert str(ex_info.value) == "Failed to translate reference path 'child/CRTest4/@child/CRTest/@value', class mismtach, expecting 'CRTest4', found 'CRTest2'"

  with pytest.raises(self.managers.cross_references.PathError) as ex_info:
    instance, attribute = self.managers.cross_references.get_by_path("CRTest3", "name3", "child/CRTest2/@childXXX/CRTest/@value")
  assert str(ex_info.value) == "Failed to translate reference path 'child/CRTest2/@childXXX/CRTest/@value', attribute 'childXXX' was not found"

  with pytest.raises(self.managers.cross_references.PathError) as ex_info:
    instance, attribute = self.managers.cross_references.get_by_path("CRTest3", "name3", "child/CRTest2//CRTest/@value")
  assert str(ex_info.value) == "Failed to translate reference path 'child/CRTest2//CRTest/@value', attribute '' was not found"

  with pytest.raises(self.managers.cross_references.PathError) as ex_info:
    instance, attribute = self.managers.cross_references.get_by_path("CRTest3", "name3", "child/CRTest2/child/CRTest")
  assert str(ex_info.value) == "Failed to translate reference path 'child/CRTest2/child/CRTest', format error"
