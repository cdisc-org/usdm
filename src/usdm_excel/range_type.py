import re
from usdm_excel.cdisc_ct import CDISCCT

class RangeType():

  def __init__(self, range_info):
    try:
      self.upper = None
      self.lower = None
      self.units = None
      self.units_code = None
      self.errors = []
      self.label = range_info.strip()
      if range_info:
        match = re.match(r"(?P<lower>[+|-]*\d+)(\s*\.\.\s*(?P<upper>[+|-]*\d+))?( \s*(?P<units>.+))?", self.label)
        if match :
          parts = match.groupdict()
          self.lower = parts['lower'].strip()
          if parts['upper']:
            self.upper = parts['upper'].strip()
          else:
            self.upper = self.lower
          if parts['units']:
            self.units = parts['units'].strip()
            self.units_code = CDISCCT().code_for_unit(self.units)
            if not self.units_code:        
              self.errors.append(f"Unable to set the units code for the range '{range_info}'")
        else:
          self.errors.append(f"Could not decode the range value, not all required parts detected in '{range_info}'")
      else:
        self.errors.append(f"Could not decode the range value, appears to be empty '{range_info}'")
    except Exception as e:
      self.errors.append(f"Exception [{e}] raised decoding range '{range_info}")

