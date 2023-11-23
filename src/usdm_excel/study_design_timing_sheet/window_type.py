import re
from usdm_excel.iso_8601_duration import ISO8601Duration
from usdm_excel.range_type import RangeType

class WindowType():

  def __init__(self, timing_info):
    self.upper = None
    self.lower = None
    self.errors = []
    self.label = timing_info.strip()
    if self.label:
      range = RangeType(self.label)
      #print(f"RANGE: {range.lower} {range.upper} {range.units} {range.units_code} {range.errors}")
      if not range.errors:
        self.lower = self._set_encoded(range.lower, range.units)
        self.upper = self._set_encoded(range.upper, range.units)     
      else:
        self.errors = range.errors

  def _set_encoded(self, value, units):
    for char in ['+', '-']:
      if char in value:
        value = value.replace(char, "")
    value = ISO8601Duration().encode(value, units)
    return value
