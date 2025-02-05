from usdm_excel.option_manager import *


def test_create(globals):
    object = OptionManager(globals)
    assert len(object._items.keys()) == 0
    assert object._items == {}


def test_set(globals):
    globals.option_manager._items = {}
    globals.option_manager.set("fred", "value")
    assert len(globals.option_manager._items.keys()) == 1
    assert globals.option_manager._items["fred"] == "value"


def test_get(globals):
    globals.option_manager._items = {}
    globals.option_manager._items["fred"] = "value"
    assert globals.option_manager.get("fred") == "value"


def test_clear(globals):
    globals.option_manager._items = {}
    globals.option_manager._items["fred"] = "value"
    assert len(globals.option_manager._items.keys()) == 1
    globals.option_manager.clear()
    assert len(globals.option_manager._items.keys()) == 0


def test_options(globals):
    globals.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.NONE)
    assert globals.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.NONE.value
    globals.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.EMPTY)
    assert globals.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value
