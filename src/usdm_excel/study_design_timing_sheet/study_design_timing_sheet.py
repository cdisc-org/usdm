from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
from usdm_excel.iso_8601_duration import ISO8601Duration
from usdm_excel.study_design_timing_sheet.window_type import WindowType
from usdm_excel.cdisc_ct import CDISCCT
from usdm_model.timing import Timing
import traceback
import re

class StudyDesignTimingSheet(BaseSheet):

  # name: TIMING_1
  # description: 3 days before, +/- 1 day
  # label: 3D +/- 1D
  # type: Before
  # from: <activity instance name ref>
  # to: <activity instance name ref>
  # timingValue: 3 days (encode to duration)
  # toFrom: Start to Start, Start to End, End to Start, End to End (S2S default)
  # window: -1..+1 Day (encode to durations)
  #
  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignTiming', optional=True)
      self.items = []
      if self.success:
        for index, row in self.sheet.iterrows():
          name = self.read_cell_by_name(index, 'name')
          description = self.read_description_by_name(index, 'description')
          label = self.read_cell_by_name(index, 'label')
          type = self._set_type(self.read_cell_by_name(index, 'type'))
          from_name = self.read_cell_by_name(index, 'from')
          to_name = self.read_cell_by_name(index, 'to')
          timing_value = self._set_text_and_encoded(self.read_cell_by_name(index, 'timingValue'))
          to_from_type = self._set_to_from_type(self.read_cell_by_name(index, 'toFrom'))
          window = WindowType(self.read_cell_by_name(index, 'window'))
          if window.errors:
            self._add_errors(window.errors, index, self._get_column_index('window'))
          try:
            item = Timing(
              id=id_manager.build_id(Timing),
              type=type,
              timingValue=timing_value,
              name=name,
              description=description,
              label=label,
              timingRelativeToFrom=to_from_type,
              timingWindow=window.label,
              timingWindowLower=window.lower,
              timingWindowUpper=window.upper,
              relativeFromScheduledInstanceId=from_name,
              relativeToScheduledInstanceId=to_name
            )
          except Exception as e:
            self._general_error(f"Failed to create Timing object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            self.items.append(item)
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

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
        return ISO8601Duration().encode(duration_parts[0].strip(), duration_parts[1].strip())
      except Exception as e:
        self._log_error(f"Could not decode the duration value '{the_duration}'")
    else:
      self._log_error(f"Could not decode the duration value, no value and units found in '{the_duration}'")

  def _set_type(self, text):
    type_code = {
      "FIXED": {'c_code': 'C99901x3', 'pt': 'Fixed Reference'},
      "AFTER": {'c_code': 'C99901x1', 'pt': 'After'},
      "BEFORE": {'c_code': 'C99901x2', 'pt': 'Before'}
    }   
    key = text.strip().upper()
    return CDISCCT().code(type_code[key]['c_code'], type_code[key]['pt'])

  def _set_to_from_type(self, text):
    type_code = {
      "S2S": {'c_code': 'C99900x1', 'pt': 'Start to Start'},
      "S2E": {'c_code': 'C99900x2', 'pt': 'Start to End'},
      "E2S": {'c_code': 'C99900x3', 'pt': 'End to Start'},
      "E2E": {'c_code': 'C99900x4', 'pt': 'End to End'},
    }    
    key = "S2S" if not text else text.strip().upper()
    return CDISCCT().code(type_code[key]['c_code'], type_code[key]['pt'])
