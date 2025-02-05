import re
import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.iso_8601_duration import ISO8601Duration
from usdm_excel.study_design_timing_sheet.window_type import WindowType
from usdm_excel.cdisc_ct import CDISCCT
from usdm_model.timing import Timing
from usdm_excel.globals import Globals


class StudyDesignTimingSheet(BaseSheet):
    SHEET_NAME = "studyDesignTiming"

    def __init__(self, file_path: str, globals: Globals):
        try:
            self.items = []
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=self.SHEET_NAME,
                optional=True,
            )
            if self.success:
                for index, row in self.sheet.iterrows():
                    name = self.read_cell_by_name(index, "name")
                    description = self.read_cell_by_name(index, "description")
                    label = self.read_cell_by_name(index, "label")
                    type = self._set_type(self.read_cell_by_name(index, "type"))
                    from_name = self.read_cell_by_name(index, "from")
                    to_name = self.read_cell_by_name(index, "to")
                    timing_label = self.read_cell_by_name(index, "timingValue")
                    timing_value = self._set_text_and_encoded(
                        self.read_cell_by_name(index, "timingValue")
                    )
                    to_from_type = self._set_to_from_type(
                        self.read_cell_by_name(index, "toFrom")
                    )
                    window = WindowType(
                        self.read_cell_by_name(index, "window"), self.globals
                    )
                    if window.errors:
                        self._add_errors(
                            window.errors, index, self._get_column_index("window")
                        )
                    try:
                        item = Timing(
                            id=self.globals.id_manager.build_id(Timing),
                            type=type,
                            value=timing_value,
                            valueLabel=timing_label,
                            name=name,
                            description=description,
                            label=label,
                            relativeToFrom=to_from_type,
                            windowLabel=window.label,
                            windowLower=window.lower,
                            windowUpper=window.upper,
                            relativeFromScheduledInstanceId=from_name,
                            relativeToScheduledInstanceId=to_name,
                        )
                    except Exception as e:
                        self._general_exception(f"Failed to create Timing object", e)
                    else:
                        self.globals.cross_references.add(name, item)
                        self.items.append(item)
        except Exception as e:
            self._sheet_exception(e)

    def _set_text_and_encoded(self, duration):
        the_duration = duration.strip()
        original_duration = the_duration
        for char in ["+", "-"]:
            if char in the_duration:
                the_duration = the_duration.replace(char, "")
                self._general_warning(f"Ignoring '{char}' in {original_duration}")
        duration_parts = re.findall(r"[^\W\d_]+|\d+", the_duration)
        if len(duration_parts) == 2:
            try:
                return ISO8601Duration().encode(
                    duration_parts[0].strip(), duration_parts[1].strip()
                )
            except Exception as e:
                self._general_error(
                    f"Could not decode the duration value '{the_duration}'"
                )
        else:
            self._general_error(
                f"Could not decode the duration value, no value and units found in '{the_duration}'"
            )

    def _set_type(self, text):
        type_code = {
            "FIXED": {"c_code": "C201358", "pt": "Fixed Reference"},
            "AFTER": {"c_code": "C201356", "pt": "After"},
            "BEFORE": {"c_code": "C201357", "pt": "Before"},
        }
        key = text.strip().upper()
        return CDISCCT(self.globals).code(
            type_code[key]["c_code"], type_code[key]["pt"]
        )

    def _set_to_from_type(self, text):
        type_code = {
            "S2S": {"c_code": "C201355", "pt": "Start to Start"},
            "S2E": {"c_code": "C201354", "pt": "Start to End"},
            "E2S": {"c_code": "C201353", "pt": "End to Start"},
            "E2E": {"c_code": "C201352", "pt": "End to End"},
        }
        key = "S2S" if not text else text.strip().upper()
        return CDISCCT(self.globals).code(
            type_code[key]["c_code"], type_code[key]["pt"]
        )
