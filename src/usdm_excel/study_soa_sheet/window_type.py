import re
from usdm_excel.iso_8601_duration import ISO8601Duration

class WindowType():

  def __init__(self, parent, row_index, col_index):
    self.__parent = parent
    self.__row = row_index
    self.__col = col_index
    self.description = ""
    self.upper = None
    self.lower = None
    timing_info = self.__parent.read_cell(row_index, col_index)
    self.description = timing_info.strip()
    if timing_info:
      timing_parts = re.split("[\s]", self.description)
      if len(timing_parts) == 4:
        self.lower = self._set_encoded(f"{timing_parts[0]}{timing_parts[3]}")
        self.upper = self._set_encoded(f"{timing_parts[2]}{timing_parts[3]}")     
      else:
        self._log_error(f"Could not decode the window value, not all required parts detected in '{timing_info}'")
    else:
      self._log_error(f"Could not decode the window value, cell was empty")
 
  def _set_encoded(self, duration):
    the_duration = duration.strip()
    original_duration = the_duration
    for char in ['+', '-']:
      if char in the_duration:
        the_duration = the_duration.replace(char, "")
        self._log_warning(f"Ignoring '{char}' in {original_duration}")
    duration_parts = re.findall(r"[^\W\d_]+|\d+", the_duration)
    if len(duration_parts) == 2:
      try:
        value = ISO8601Duration().encode(duration_parts[0].strip(), duration_parts[1].strip())
        return value
      except Exception as e:
        self._log_error(f"Could not decode the duration value '{the_duration}'")
        return ""
    else:
      self._log_error(f"Could not decode the duration value, no value and units found in '{the_duration}'")
      return ""

  def _log_error(self, message):
    self.__parent._error(self.__row, self.__col, message)

  def _log_warning(self, message):
    self.__parent._warning(self.__row, self.__col, message)