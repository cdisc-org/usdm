class ISO8601Duration():
  
  ZERO_DURATION = "PT0M"

  def __init__(self):
    pass

  def encode(self, value, unit):
    the_value = int(value.strip())
    unit_text = unit.strip()
    if unit_text.upper() in ['YRS', 'Y', 'YEARS']:
      return f"P{the_value}Y"
    if unit_text.upper() in ['MTHS', 'MTH', 'MONTHS']:
      return f"P{the_value}M"
    if unit_text.upper() in ['D', 'DAYS']:
      return f"P{the_value}D"
    if unit_text.upper() in ['H', 'HRS', 'HOURS']:
      return f"PT{the_value}H"
    if unit_text.upper() in ['M', 'MINS', 'MINUTES']:
      return f"PT{the_value}M"
    if unit_text.upper() in ['S', 'SECS', 'SECONDS']:
      return f"PT{the_value}S"
    raise ValueError
  