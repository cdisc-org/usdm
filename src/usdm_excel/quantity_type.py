import re
from usdm_excel.cdisc_ct import CDISCCT

class QuantityType():

  def __init__(self, quantity_info, units_reqd=True, allow_empty=True):
    try:
      self.value = None
      self.units = None
      self.units_code = None
      self.errors = []
      self.empty = False
      self.label = quantity_info.strip()
      if quantity_info:
        match = re.match(r"(?P<value>[+|-]*\d+)( \s*(?P<units>.+))?", self.label)
        if match :
          parts = match.groupdict()
          self.value = parts['value'].strip()
          if units_reqd:
            if parts['units']:
              self.units = parts['units'].strip()
              self.units_code = CDISCCT().code_for_unit(self.units)
              if not self.units_code:        
                self.errors.append(f"Unable to set the units code for the quantity '{quantity_info}'")
            else:
              self.errors.append(f"Could not decode the quantity value, possible typographical errors '{quantity_info}'")
        else:
          self.errors.append(f"Could not decode the quantity value '{quantity_info}'")
      elif not allow_empty:
        self.errors.append(f"Could not decode the quantity value, appears to be empty '{quantity_info}'")
      else:
        self.empty = True
    except Exception as e:
      self.errors.append(f"Exception '{e}' raised decoding quantity '{quantity_info}")

