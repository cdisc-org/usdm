import re
from usdm_excel.iso_8601_duration import ISO8601Duration

class WindowType():

  def __init__(self, timing_info):
    self.upper = None
    self.lower = None
    self.errors = []
    self.label = timing_info.strip()
    if timing_info:
      match = re.match(r"(?P<lower>[+|-]*\d+)\s*\.\.\s*(?P<upper>[+|-]*\d+) \s*(?P<units>.+)", self.label)
      if match is not None:
        timing_parts = match.groupdict()
        self.lower = self._set_encoded(f"{timing_parts['lower']}{timing_parts['units']}")
        self.upper = self._set_encoded(f"{timing_parts['upper']}{timing_parts['units']}")     
      else:
        self.errors.append(f"Could not decode the window value, not all required parts detected in '{timing_info}'")
    else:
      pass # Empty, this is OK

  def _set_encoded(self, duration):
    the_duration = duration.strip()
    original_duration = the_duration
    for char in ['+', '-']:
      if char in the_duration:
        the_duration = the_duration.replace(char, "")
        #self.warnings.append(f"Ignoring '{char}' in {original_duration}")
    duration_parts = re.findall(r"[^\W\d_]+|\d+", the_duration)
    if len(duration_parts) == 2:
      try:
        value = ISO8601Duration().encode(duration_parts[0].strip(), duration_parts[1].strip())
        return value
      except Exception as e:
        self.errors.append(f"Could not decode the duration value '{the_duration}'")
        return ""
    else:
      self.errors.append(f"Could not decode the duration value, no value and units found in '{the_duration}'")
      return ""
