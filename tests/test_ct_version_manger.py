from usdm_excel.ct_version_manager import *


def test_create(globals):
    object = CTVersionManager(globals)
    assert len(object._items.keys()) == 0
    assert object._items == {}


def test_add(globals):
    globals.ct_version_manager._items = {}
    globals.ct_version_manager.add("fred", "value")
    assert len(globals.ct_version_manager._items.keys()) == 1
    assert globals.ct_version_manager._items["FRED"] == "value"
    globals.ct_version_manager.add("Sid1", "value")
    assert len(globals.ct_version_manager._items.keys()) == 2
    assert globals.ct_version_manager._items["SID1"] == "value"


def test_get(globals):
    globals.ct_version_manager._items = {}
    globals.ct_version_manager._items["FRED"] = "value"
    assert globals.ct_version_manager.get("fred") == "value"
    assert globals.ct_version_manager.get("FRED") == "value"


def test_clear(globals):
    globals.ct_version_manager._items = {}
    globals.ct_version_manager._items["fred"] = "value"
    assert len(globals.ct_version_manager._items.keys()) == 1
    globals.ct_version_manager.clear()
    assert len(globals.ct_version_manager._items.keys()) == 0
