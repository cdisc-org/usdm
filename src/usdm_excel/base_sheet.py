import pandas as pd
from usdm_excel.id_manager import id_manager
from usdm_excel.cdisc_ct import CDISCCT
from usdm_model.code import Code
from usdm_excel.ct_version_manager import ct_version_manager
from usdm_excel.errors.errors import error_manager
from usdm_excel.logger import package_logger
from usdm_excel.option_manager import *

class BaseSheet():

  def __init__(self, file_path, sheet_name, header=0):
    self.file_path = file_path
    self.sheet_name = sheet_name
    self.sheet = pd.read_excel(open(file_path, 'rb'), sheet_name=sheet_name, header=header)
    self._general_info("Processed sheet %s" % (sheet_name))

  def cell_empty(self, row_index, col_index):
    return pd.isnull(self.sheet.iloc[row_index, col_index])  

  def read_cell_by_name(self, row_index, field_name):
    try:
      col_index = self.sheet.columns.get_loc(field_name)
      return self.read_cell(row_index, col_index)
    except Exception as e:
      col_index = -2
      self._error(row_index, col_index, "Error (%s) reading cell" % (e))
      return ""

  def read_cell(self, row_index, col_index):
    try:
      if pd.isnull(self.sheet.iloc[row_index, col_index]):
        return ""
      else:
        return str(self.sheet.iloc[row_index, col_index]).strip()
    except Exception as e:
      self._error(row_index, col_index, "Error (%s) reading cell" % (e))
      return ""

  def read_cell_empty_legacy(self, row_index, col_index):
    if self.cell_empty(row_index, col_index):
      return "", True
    else:
      value = self.read_cell_empty(row_index, col_index, '-')
      if value == "":
        return "", True
      else:
        return value, False

  def read_cell_empty(self, row_index, col_index, empty_character):
    value = self.read_cell(row_index, col_index)
    value = "" if value == empty_character else value
    return value

  def read_cell_multiple(self, rindex, cindex):
    results = []
    value = self.read_cell(rindex, cindex)
    if value.strip() == '':
      return results
    for part in value.split(","):
      results.append(part.strip())
    return results

  def read_cell_with_previous(self, row_index, col_index, first_col_index):
    try:
      i = col_index
      while i >= first_col_index:
        if pd.isnull(self.sheet.iloc[row_index, i]):
          i -= 1
        else:
          return self.sheet.iloc[row_index, i].strip()
      self._error(row_index, col_index, "Blank cell error")
      return ""
    except Exception as e:
      self._error(row_index, col_index, "Error (%s) reading cell row '%s', field '%s'" % (e, row_index, col_index))
      return ""

  def read_boolean_cell_by_name(self, row_index, field_name):
    value = self.read_cell_by_name(row_index, field_name)
    if value.strip().upper() in ['Y', 'YES', 'TRUE', '1']:
      return True
    return False

  # Want to kill this method
  def set_cdisc_code(self, value):
    if value.strip() == "":
      return None
    parts = value.split("=")
    try:
      return CDISCCT().code(code=parts[0].strip(), decode=parts[1].strip())
    except Exception as e:
      self._error(0, 0, "CDISC code error '%s'" % (e))
      return None

  def read_other_code_cell_by_name(self, row_index, field_name):
    col_index = self.sheet.columns.get_loc(field_name)
    return self.read_other_code_cell(row_index, col_index)

  def read_other_code_cell(self, row_index, col_index):
    value = self.read_cell(row_index, col_index)
    if value.strip() == "":
      return None
    return self._decode_other_code(value, row_index, col_index)

  def read_other_code_cell_multiple_by_name(self, row_index, field_name):
    col_index = self.sheet.columns.get_loc(field_name)
    return self.read_other_code_cell_mutiple(row_index, col_index)

  def read_other_code_cell_mutiple(self, row_index, col_index):
    value = self.read_cell(row_index, col_index)
    result = []
    if value.strip() == '':
      return result
    items = value.split(",")
    for item in items:
      code = self._decode_other_code(item.strip(), row_index, col_index)
      if not code == None:
        result.append(code)
    return result

  def read_cdisc_klass_attribute_cell_by_name(self, klass, attribute, row_index, field_name):
    col_index = self.sheet.columns.get_loc(field_name)
    return self.read_cdisc_klass_attribute_cell(klass, attribute, row_index, col_index)

  def read_cdisc_klass_attribute_cell(self, klass, attribute, row_index, col_index):
    code = None
    value = self.read_cell(row_index, col_index)
    if value.strip() == "":
      self._error(row_index, col_index, "Empty cell detected where CDISC CT value expected.")
    else:
      code = CDISCCT().code_for_attribute(klass, attribute, value)
      if code is None:
        self._error(row_index, col_index, f"CDISC CT not found for value '{value}'.")
    return code

  def read_cdisc_klass_attribute_cell_multiple_by_name(self, klass, attribute, row_index, field_name):
    col_index = self.sheet.columns.get_loc(field_name)
    return self.read_cdisc_klass_attribute_cell_multiple(klass, attribute, row_index, col_index)

  def read_cdisc_klass_attribute_cell_multiple(self, klass, attribute, row_index, col_index):
    result = []
    value = self.read_cell(row_index, col_index)
    if value.strip() == "":
      self._error(row_index, col_index, "Empty cell detected where multiple CDISC CT values expected.")
      return result
    items = value.split(",")
    for item in items:
      code = CDISCCT().code_for_attribute(klass, attribute, item.strip())
      if code is not None:
        result.append(code)
      else:
        self._error(row_index, col_index, f"CDISC CT not found for value '{item.strip()}'.")
    return result

  def double_link(self, items, id, prev, next):
    for idx, item in enumerate(items):
      if idx == 0:
        if option_manager.get(Options.PREVIOUS_NEXT) == PrevNextOption.NULL_STRING:
          setattr(item, prev, "")
        else:
          setattr(item, prev, None)
      else:
        the_id = getattr(items[idx-1], id)
        setattr(item, prev, the_id)
      if idx == len(items)-1:  
        if option_manager.get(Options.PREVIOUS_NEXT) == PrevNextOption.NULL_STRING:
          setattr(item, next, "")
        else:
          setattr(item, next, None)
      else:
        the_id = getattr(items[idx+1], id)
        setattr(item, next, the_id)

  def _decode_other_code(self, value, row_index, col_index):
    if value.strip() == "":
      return None
    outer_parts = value.split(":")
    if len(outer_parts) == 2:
      system = outer_parts[0].strip()
      inner_parts = outer_parts[1].strip().split("=")
      if len(inner_parts) == 2:
        version = ct_version_manager.get(system)
        return Code(codeId=id_manager.build_id(Code), code=inner_parts[0].strip(), codeSystem=system, codeSystemVersion=version, decode=inner_parts[1].strip())
      else:
        self._error(row_index, col_index, "Failed to decode code data '%s', no '=' detected" % (value))
    else:
      self._error(row_index, col_index, "Failed to decode code data '%s', no ':' detected" % (value))
    return None

  def _info(self, row, column, message):
     package_logger.info(self._format(row + 1, column + 1, message))
     
  def _general_info(self, message):
     package_logger.info(self._format(None, None, message))
     
  def _error(self, row, column, message):
    error_manager.add(self.sheet_name, row + 1, column + 1, message)

  def _general_error(self, message):
    error_manager.add(self.sheet_name, None, None, message)

  def _warning(self, row, column, message):
    error_manager.add(self.sheet_name, row + 1, column + 1, message, error_manager.WARNING)

  def _traceback(self, message):
    package_logger.debug(message)

  def _format(self, row, column, message):
    if self.sheet_name == None:
      return f"{self.message}"
    elif row == None:
      return f"In sheet {self.sheet_name}: {message}"
    else:
      return f"In sheet {self.sheet_name} at [{row},{column}]: {message}"
