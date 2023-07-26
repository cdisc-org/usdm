import re
from usdm_excel.iso_8601_duration import ISO8601Duration

class TimepointType():

  def __init__(self, parent, row_index, col_index):
    self.timing_type = None
    self.relative_ref = 0
    self.description = None
    self.value = ISO8601Duration.ZERO_DURATION
    if parent is not None:
      self.__parent = parent
      self.__row = row_index
      self.__col = col_index
      timing_info = self.__parent.read_cell(row_index, col_index)
      if timing_info:
        timing_parts = timing_info.split(":")
        if len(timing_parts) == 2:
          if timing_parts[0].upper()[0] == "A":
            self.timing_type = "anchor"
            self.relative_ref = 0
          if timing_parts[0].upper()[0] == "P":
            self.timing_type = "previous"
            self.relative_ref = self._get_relative_ref(timing_parts[0]) * -1
            self._set_text_and_encoded(timing_parts[1])
          elif timing_parts[0].upper()[0] == "N":
            self.timing_type = "next"
            self.relative_ref = self._get_relative_ref(timing_parts[0])
            self._set_text_and_encoded(timing_parts[1])
          elif timing_parts[0].upper()[0] == "C":
            self.timing_type = "cycle start"
            self.relative_ref = self._get_relative_ref(timing_parts[0])
            self._set_text_and_encoded(timing_parts[1])
        else:
          self._log_error(f"Could not decode the timing value, no ':' detected in '{timing_info}'")
      else:
        self._log_error(f"Could not decode the timing value, cell was empty")
    
  def set_type(self, type, value, cycle):
    self.timing_type = type

  def _set_text_and_encoded(self, duration):
    the_duration = duration.strip()
    original_duration = the_duration
    for char in ['+', '-']:
      if char in the_duration:
        the_duration = the_duration.replace(char, "")
        self._log_warning(f"Ignoring '{char}' in {original_duration}")
    duration_parts = re.findall(r"[^\W\d_]+|\d+", the_duration)
    if len(duration_parts) == 2:
      try:
        self.description = original_duration
        self.value = ISO8601Duration().encode(duration_parts[0].strip(), duration_parts[1].strip())
      except Exception as e:
        self._log_error(f"Could not decode the duration value '{the_duration}'")
    else:
      self._log_error(f"Could not decode the duration value, no value and units found in '{the_duration}'")

  def _get_relative_ref(self, part):
    part = part.strip()
    return int(part[1:]) if len(part) > 1 else 1
  
  def _log_error(self, message):
    self.__parent._error(self.__row, self.__col, message)

  def _log_warning(self, message):
    self.__parent._warning(self.__row, self.__col, message)