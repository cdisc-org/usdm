class ISO8601Duration:
    ZERO_DURATION = "PT0M"

    def __init__(self):
        pass

    def encode(self, value, unit):
        the_value = int(value.strip())
        unit_text = unit.strip()
        if unit_text.upper() in ["Y", "YRS", "YR", "YEARS", "YEAR"]:
            return f"P{the_value}Y"
        if unit_text.upper() in ["MTHS", "MTH", "MONTHS", "MONTH"]:
            return f"P{the_value}M"
        if unit_text.upper() in ["W", "WKS", "WK", "WEEKS", "WEEK"]:
            return f"P{the_value}W"
        if unit_text.upper() in ["D", "DYS", "DY", "DAYS", "DAY"]:
            return f"P{the_value}D"
        if unit_text.upper() in ["H", "HRS", "HR", "HOURS", "HOUR"]:
            return f"PT{the_value}H"
        if unit_text.upper() in ["M", "MINS", "MIN", "MINUTES", "MINUTE"]:
            return f"PT{the_value}M"
        if unit_text.upper() in ["S", "SECS", "SEC", "SECONDS", "SECOND"]:
            return f"PT{the_value}S"
        raise ValueError
