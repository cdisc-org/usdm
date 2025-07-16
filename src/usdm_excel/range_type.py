import re
from usdm_excel.globals import Globals
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.alias import Alias


class RangeType:
    def __init__(
        self,
        range_info: str,
        globals: Globals,
        units_reqd: bool = True,
        allow_empty: bool = True,
    ):
        try:
            self.upper = None
            self.lower = None
            self.units = None
            self.upper_units_code = None
            self.lower_units_code = None
            self.errors = []
            self.empty = False
            self.label = range_info.strip()
            if range_info:
                match = re.match(
                    r"(?P<lower>[+|-]*\d+)(\s*\.\.\s*(?P<upper>[+|-]*\d+))?( \s*(?P<units>.+))?",
                    self.label,
                )
                if match:
                    parts = match.groupdict()
                    self.lower = parts["lower"].strip()
                    if parts["upper"]:
                        self.upper = parts["upper"].strip()
                    else:
                        self.upper = self.lower
                    if units_reqd:
                        if parts["units"]:
                            self.units = parts["units"].strip()
                            # Units code now an alias. Duplicates created so separate ids are used
                            lower_cdisc_code = CDISCCT(globals).code_for_unit(
                                self.units
                            )
                            upper_cdisc_code = CDISCCT(globals).code_for_unit(
                                self.units
                            )
                            self.lower_units_code = Alias(globals).code(
                                lower_cdisc_code, []
                            )
                            self.upper_units_code = Alias(globals).code(
                                upper_cdisc_code, []
                            )
                            if not self.lower_units_code or not self.upper_units_code:
                                self.errors.append(
                                    f"Unable to set the units code for the range '{range_info}'"
                                )
                        else:
                            self.errors.append(
                                f"Could not decode the range value, possible typographical errors '{range_info}'"
                            )
                else:
                    self.errors.append(
                        f"Could not decode the range value '{range_info}'"
                    )
            elif not allow_empty:
                self.errors.append(
                    f"Could not decode the range value, appears to be empty '{range_info}'"
                )
            else:
                self.empty = True
        except Exception as e:
            self.errors.append(f"Exception '{e}' raised decoding range '{range_info}")
