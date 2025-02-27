from tests.test_factory import Factory
from usdm_excel.quantity_type import QuantityType


def test_quantity_type(mocker, globals):
    test_data = [
        ("15 days", "15", "days", "C25301", "15 days"),
        ("1%", "1", "%", "C25613", "1%"),
        ("  10    %", "10", "%", "C25613", "10    %"),
        ("  10.0    %", "10", "%", "C25613", "10.0    %"),
    ]
    for index, test in enumerate(test_data):
        item = QuantityType(test[0], globals)
        assert (item.value) == test[1]
        assert (item.units) == test[2]
        assert (item.units_code.code) == test[3]
        assert (item.errors) == []
        assert (item.empty) == False
        assert (item.label) == test[4]


def test_quantity_type_empty(mocker, globals):
    test_data = [
        ("15 days", "15", "days", "C25301", False, "15 days"),
        ("", None, None, None, True, ""),
    ]
    for index, test in enumerate(test_data):
        item = QuantityType(test[0], globals, allow_empty=True)
        assert (item.value) == test[1]
        assert (item.units) == test[2]
        if test[3]:
            assert (item.units_code.code) == test[3]
        else:
            assert (item.units_code) == test[3]
        assert (item.errors) == []
        assert (item.empty) == test[4]
        assert (item.label) == test[5]


def test_quantity_type_no_units(mocker, globals):
    test_data = [
        (" 15 ", "15", None, None, False, "15"),
        (" 15 C ", "15", "C", "C42559", False, "15 C"),
        (" 15.0 ", "15", None, None, False, "15.0"),
    ]
    for index, test in enumerate(test_data):
        # print(f"TEST {test}")
        item = QuantityType(test[0], globals, allow_missing_units=True)
        assert (item.value) == test[1]
        assert (item.units) == test[2]
        if test[3]:
            assert (item.units_code.code) == test[3]
        else:
            assert (item.units_code) == test[3]
        assert (item.errors) == []
        assert (item.empty) == test[4]
        assert (item.label) == test[5]


def test_range_type_error(mocker, globals):
    test_data = [
        (" Days", False, False, "Could not decode the quantity value ' Days'"),
        (
            "1",
            False,
            False,
            "Could not decode the quantity value, possible typographical errors '1'",
        ),
        ("abc", False, False, "Could not decode the quantity value 'abc'"),
        (
            "10 slugs",
            False,
            False,
            "Unable to set the units code for the quantity '10 slugs'",
        ),
    ]
    for index, test in enumerate(test_data):
        item = QuantityType(
            test[0], globals, allow_missing_units=test[1], allow_empty=test[2]
        )
        assert item.errors == [test[3]]
