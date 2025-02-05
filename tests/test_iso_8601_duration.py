import pytest
from usdm_excel.iso_8601_duration import ISO8601Duration


def test_encode(mocker, globals):
    item = ISO8601Duration()
    assert item.encode("1", "y") == "P1Y"
    assert item.encode("2", "yeaR") == "P2Y"
    assert item.encode("2", "years") == "P2Y"
    assert item.encode("3", "yrs") == "P3Y"
    assert item.encode("3", "yr") == "P3Y"
    assert item.encode("1", "MTHS") == "P1M"
    assert item.encode("1", "MTH") == "P1M"
    assert item.encode("2", "mOnth") == "P2M"
    assert item.encode("2", "months") == "P2M"
    assert item.encode("12", "week") == "P12W"
    assert item.encode("12", "weeks") == "P12W"
    assert item.encode("13", "Wks") == "P13W"
    assert item.encode("13", "Wk") == "P13W"
    assert item.encode("1 ", "W") == "P1W"
    assert item.encode("1", "d") == "P1D"
    assert item.encode("12", "days") == "P12D"
    assert item.encode("12", "dys") == "P12D"
    assert item.encode("12", "dy") == "P12D"
    assert item.encode("13", "DAY") == "P13D"
    assert item.encode("1 ", "Hours") == "PT1H"
    assert item.encode("1 ", "Hour") == "PT1H"
    assert item.encode("1 ", "HRS") == "PT1H"
    assert item.encode("1 ", "HR") == "PT1H"
    assert item.encode(" 2", "H") == "PT2H"
    assert item.encode("  3  ", "H") == "PT3H"
    assert item.encode("1 ", "Mins") == "PT1M"
    assert item.encode("1 ", "MiN") == "PT1M"
    assert item.encode(" 2", "M") == "PT2M"
    assert item.encode("  322  ", "minutes") == "PT322M"
    assert item.encode("  322  ", "minute") == "PT322M"
    assert item.encode("1 ", "secS") == "PT1S"
    assert item.encode("1 ", "seC") == "PT1S"
    assert item.encode(" 2", "S") == "PT2S"
    assert item.encode("  322  ", "Seconds") == "PT322S"
    assert item.encode("  322  ", "Second") == "PT322S"
    with pytest.raises(Exception):
        item.encode("  322  ", "XSeconds")
