from usdm_excel.iso_8601_duration import ISO8601Duration
from usdm_excel.range_type import RangeType
from usdm_excel.globals import Globals


class WindowType:
    def __init__(self, timing_info: str, globals: Globals):
        self.upper = None
        self.lower = None
        self.errors = []
        self.label = timing_info.strip() if timing_info else ""
        if self.label:
            range = RangeType(self.label, globals)
            if not range.errors:
                self.lower = self._set_encoded(range.lower, range.units)
                self.upper = self._set_encoded(range.upper, range.units)
            else:
                self.errors = range.errors

    def _set_encoded(self, value, units):
        for char in ["+", "-"]:
            if char in value:
                value = value.replace(char, "")
        value = ISO8601Duration().encode(value, units)
        return value
