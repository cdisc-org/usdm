from tests.test_factory import Factory
from usdm_excel.range_type import RangeType


def test_range_type(mocker, globals):
    test_data = [
        ("1..1 Days", "1", "1", "1..1 Days", "Days", "C25301"),
        (" -1..1 days", "-1", "1", "-1..1 days", "days", "C25301"),
        ("5 .. 10 weeks ", "5", "10", "5 .. 10 weeks", "weeks", "C29844"),
    ]
    for index, test in enumerate(test_data):
        item = RangeType(test[0], globals)
        assert (item.lower) == test[1]
        assert (item.upper) == test[2]
        assert (item.label) == test[3]
        assert (item.units) == test[4]
        assert (item.lower_units_code.standardCode.code) == test[5]
        assert (item.upper_units_code.standardCode.code) == test[5]
        assert (item.errors) == []


def test_range_type_error(mocker, globals):
    test_data = [
        (
            "1.. Days",
            "Could not decode the range value, possible typographical errors '1.. Days'",
        ),
        (
            "-1.1 days",
            "Could not decode the range value, possible typographical errors '-1.1 days'",
        ),
        (
            "-1 .. 1",
            "Could not decode the range value, possible typographical errors '-1 .. 1'",
        ),
        (" .. 1 Weeks", "Could not decode the range value ' .. 1 Weeks'"),
        ("1 .. 10 slugs", "Unable to set the units code for the range '1 .. 10 slugs'"),
    ]
    for index, test in enumerate(test_data):
        item = RangeType(test[0], globals)
        assert item.errors == [test[1]]
