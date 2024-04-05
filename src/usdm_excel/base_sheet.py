import os
import logging
import traceback
import pandas as pd
from openpyxl import load_workbook
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.other_ct import OtherCT
##from usdm_excel.id_manager import id_manager
#from usdm_excel.ct_version_manager import ct_version_manager
#from usdm_excel.errors.errors import error_manager
#from usdm_excel.logger import package_logger
##from usdm_excel.cross_ref import cross_references
from usdm_excel.option_manager import Options
from usdm_excel.quantity_type import QuantityType
from usdm_excel.range_type import RangeType
from usdm_excel.iso_3166 import ISO3166
from usdm_model.quantity import Quantity
from usdm_model.range import Range
from usdm_model.address import Address
from usdm_excel.alias import Alias

class BaseSheet():

  class StateError(Exception):
    pass

  class FormatError(Exception):
    pass

  def __init__(self, file_path, managers, sheet_name, header=0, optional=False, converters={}, require={}):
    self.file_path = file_path
    self.managers = managers
    self.dir_path, self.filename = os.path.split(file_path)
    self.sheet_name = sheet_name
    self.sheet = None
    self.success = False
    if optional and not self._sheet_present(file_path, sheet_name):
      self._general_info(f"{sheet_name} not found but optional")
    else:
      if require and not self._check_cell_value(file_path, sheet_name, require['row'], require['column'], require['value']):
        self._general_info(f"Required value {require['value']} at [{require['row']}, {require['column']}] mismatch in {sheet_name}")
        pass
      else:
        self.sheet = pd.read_excel(open(file_path, 'rb'), sheet_name=sheet_name, header=header, converters=converters)
        self.success = True
        self._general_info("Processed sheet %s" % (sheet_name))

  def cell_empty(self, row_index, col_index):
    return pd.isnull(self.sheet.iloc[row_index, col_index])  

  def column_present(self, names):
    fields = [names] if isinstance(names, str) else names
    for field in fields:
      try:
        col_index = self.sheet.columns.get_loc(field)
        return col_index
      except:
        pass
    raise BaseSheet.FormatError(f"Failed to detect column(s) '{', '.join(fields)}' in sheet")

  def read_cell_by_name(self, row_index, field_name, default=None, must_be_present=True):
    try:
      col_index = self.column_present(field_name)
      return self.read_cell(row_index, col_index)
    except Exception as e:
      if not must_be_present:
        return "" #if self.managers.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value else None
      elif default:
        return default
      else:
        self._error(row_index, -2, f"Error '{e}' reading cell '{field_name}'")
        return "" #if self.managers.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value else None

  def read_cell(self, row_index, col_index, default=None):
    try:
      if pd.isnull(self.sheet.iloc[row_index, col_index]):
        if default:
          return default
        else:
          return "" #if self.managers.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value else None
      else:
        return str(self.sheet.iloc[row_index, col_index]).strip()
    except Exception as e:
      self._error(row_index, col_index, f"Error '{e}' reading cell")
      self._traceback(f"{e}\n{traceback.format_exc()}")
      if default:
        return default
      else:
        return "" #if self.managers.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value else None

  # Deprecate this method
  def read_cell_empty_legacy(self, row_index, col_index):
    if self.cell_empty(row_index, col_index):
      return "", True
    else:
      value = self.read_cell_empty(row_index, col_index, '-')
      if value == "":
        return "", True
      else:
        return value, False

  # Deprecate this method
  def read_cell_empty(self, row_index, col_index, empty_character):
    value = self.read_cell(row_index, col_index)
    value = "" if (value == empty_character) or (value == None) else value
    return value

  def read_cell_multiple(self, rindex, cindex):
    try:
      results = []
      value = self.read_cell(rindex, cindex)
      if value.strip() == '':
        return results
      for part in self._state_split(value):
        results.append(part.strip())
      return results
    except BaseSheet.StateError as e:
      self._error(rindex, cindex, f"Internal state error '{e}' reading cell")
    except BaseSheet.FormatError as e:
      self._error(rindex, cindex, "Format error reading cell, check the format of the cell")

  def read_cell_with_previous(self, row_index, col_index, first_col_index):
    try:
      i = col_index
      while i >= first_col_index:
        if pd.isnull(self.sheet.iloc[row_index, i]):
          i -= 1
        else:
          return self.sheet.iloc[row_index, i].strip()
      self._warning(row_index, col_index, "No previous non-empty cell found.")
      return ""
    except Exception as e:
      self._error(row_index, col_index, "Error (%s) reading cell row '%s', field '%s'" % (e, row_index, col_index))
      return ""

  def read_boolean_cell_by_name(self, row_index, field_name, must_be_present=True):
    value = self.read_cell_by_name(row_index, field_name, must_be_present=must_be_present)
    if not value:
      return False
    elif value.strip().upper() in ['Y', 'YES', 'T', 'TRUE', '1']:
      return True
    return False

  def read_quantity_cell_by_name(self, row_index, field_name, allow_missing_units=True, allow_empty=True):
    col_index = self.column_present(field_name)
    return self.read_quantity_cell(row_index, col_index, allow_missing_units, allow_empty)

  def read_quantity_cell(self, row_index, col_index, allow_missing_units=True, allow_empty=True):
    try:
      text = self.read_cell(row_index, col_index)
      quantity = QuantityType(text, allow_missing_units, allow_empty)
      if not quantity.errors:
        unit = Alias.code(quantity.units_code, [])
        return None if quantity.empty else Quantity(id=self.managers.id_manager.build_id(Quantity), value=float(quantity.value), unit=unit)
      else:
        self._add_errors(quantity.errors, row_index, col_index)
        return None
    except Exception as e:
      self._error(row_index, col_index, f"Failed to decode quantity data '{text}'")
      self._traceback(f"{e}\n{traceback.format_exc()}")
      return None

  def read_range_cell_by_name(self, row_index, field_name, require_units=True, allow_empty=True):
    col_index = self.column_present(field_name)
    return self.read_range_cell(row_index, col_index, require_units, allow_empty)

  def read_range_cell(self, row_index, col_index, require_units=True, allow_empty=True):
    try:
      text = self.read_cell(row_index, col_index)
      range = RangeType(text, require_units, allow_empty)
      if not range.errors:
        #print(f"RANGE: {range.lower} {range.upper} {range.units} {range.units_code} {range.empty} ")
        return None if range.empty else Range(id=self.managers.id_manager.build_id(Range), minValue=float(range.lower), maxValue=float(range.upper), unit=range.units_code, isApproximate=False)
      else:
        self._add_errors(range.errors, row_index, col_index)
        return None
    except Exception as e:
      self._error(row_index, col_index, f"Failed to decode range data '{text}'")
      #print(f"{e}\n{traceback.format_exc()}")
      self._traceback(f"{e}\n{traceback.format_exc()}")
      return None

  def read_address_cell_by_name(self, row_index, field_name, allow_empty=False):
    raw_address = self.read_cell_by_name(row_index, field_name)
    # TODO The '|' separator is preserved for legacy reasons but should be removed in the future
    if not raw_address:
      sep = ','
      parts = []
    elif '|' in raw_address:
      sep = '|'
      parts = raw_address.split(sep)
    else:
      sep = ','
      parts = self._state_split(raw_address)
    if len(parts) == 6:
      result = self._to_address(
          self.managers.id_manager.build_id(Address),
          line=parts[0].strip(), 
          district=parts[1].strip(), 
          city=parts[2].strip(), 
          state=parts[3].strip(), 
          postal_code=parts[4].strip(), 
          country=ISO3166().code(parts[5].strip())
        )
      return result
    elif allow_empty:
      pass
    else:
      col_index = self.sheet.columns.get_loc(field_name)
      self._error(row_index, col_index, f"Address does not contain the required fields (line, district, city, state, postal code and country code) using '{sep}' separator characters, only {len(parts)} found")
      return None

  def _to_address(self, id, line, city, district, state, postal_code, country):
    text = "%s, %s, %s, %s, %s, %s" % (line, city, district, state, postal_code, country.decode)
    text = text.replace(' ,', '')
    try:
      result = Address(id=id, text=text, line=line, city=city, district=district, state=state, postalCode=postal_code, country=country)
    except Exception as e:
      self._general_error(f"Failed to create Address object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      result = None
    return result

  def create_object(self, cls, params):
    try:
      params['id'] = self.managers.id_manager.build_id(cls)
      return cls(**params)
    except Exception as e:
      self._general_error(f"Failed to create {cls.__name__} object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      return None

  def read_other_code_cell_by_name(self, row_index, field_name):
    #col_index = self.sheet.columns.get_loc(field_name)
    col_index = self.column_present(field_name)
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
    for item in self._state_split(value):
      code = self._decode_other_code(item.strip(), row_index, col_index)
      if not code == None:
        result.append(code)
    return result

  def read_cdisc_klass_attribute_cell_by_name(self, klass, attribute, row_index, field_name, allow_empty=False):
    col_index = self.column_present(field_name)
    return self.read_cdisc_klass_attribute_cell(klass, attribute, row_index, col_index, allow_empty)

  def read_cdisc_klass_attribute_cell(self, klass, attribute, row_index, col_index, allow_empty=False):
    code = None
    value = self.read_cell(row_index, col_index)
    if value:
      code = CDISCCT().code_for_attribute(klass, attribute, value)
      if not code:
        self._error(row_index, col_index, f"CDISC CT not found for value '{value}'.")
    elif not allow_empty:
      self._error(row_index, col_index, "Empty cell detected where CDISC CT value expected.")
    return code

  def read_cdisc_klass_attribute_cell_multiple_by_name(self, klass, attribute, row_index, field_name):
    #col_index = self.sheet.columns.get_loc(field_name)
    col_index = self.column_present(field_name)
    return self.read_cdisc_klass_attribute_cell_multiple(klass, attribute, row_index, col_index)

  def read_cdisc_klass_attribute_cell_multiple(self, klass, attribute, row_index, col_index):
    result = []
    value = self.read_cell(row_index, col_index)
    if value.strip() == "":
      self._error(row_index, col_index, "Empty cell detected where multiple CDISC CT values expected.")
      return result
    for item in self._state_split(value):
      code = CDISCCT().code_for_attribute(klass, attribute, item.strip())
      if code is not None:
        result.append(code)
      else:
        self._error(row_index, col_index, f"CDISC CT not found for value '{item.strip()}'.")
    return result

  def _get_cross_reference(self, klass, name, error_klass_name):
    item = self.managers.cross_references.get(klass, name)
    if item:
      return item.id
    else:
      self._general_error(f"Unable to find {error_klass_name} with name '{name}'")              
      return None

  def double_link(self, items, prev, next):
    try: 
      for idx, item in enumerate(items):
        if idx == 0:
          if self.managers.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value:
            setattr(item, prev, "")
          else:
            setattr(item, prev, None)
        else:
          the_id = getattr(items[idx-1], 'id')
          setattr(item, prev, the_id)
        if idx == len(items)-1:  
          if self.managers.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value:
            setattr(item, next, "")
          else:
            setattr(item, next, None)
        else:
          the_id = getattr(items[idx+1], 'id')
          setattr(item, next, the_id)
    except Exception as e:
      self._general_error(f"Exception '{e}' in double_link: {items}")

  def previous_link(self, items, prev):
    try: 
      for idx, item in enumerate(items):
        if idx == 0:
          if self.managers.option_manager.get(Options.EMPTY_NONE) == EmptyNoneOption.EMPTY.value:
            setattr(item, prev, "")
          else:
            setattr(item, prev, None)
        else:
          the_id = getattr(items[idx-1], 'id')
          setattr(item, prev, the_id)
    except Exception as e:
      self._general_error(f"Exception '{e}' in previous_link: {items}")

  def _decode_other_code(self, value, row_index, col_index):
    if value.strip() == "":
      return None
    outer_parts = value.split(":")
    if len(outer_parts) == 2:
      system = outer_parts[0].strip()
      inner_parts = outer_parts[1].strip().split("=")
      if len(inner_parts) == 2:
        version = ct_version_manager.get(system)
        return OtherCT().code(code=inner_parts[0].strip(), system=system, version=version, decode=inner_parts[1].strip())
      else:
        self._error(row_index, col_index, "Failed to decode code data '%s', no '=' detected" % (value))
    else:
      self._error(row_index, col_index, "Failed to decode code data '%s', no ':' detected" % (value))
    return None

  def _to_int(self, value):
    try:
      return int(value)
    except:
      return None

  def _add_errors(self, errors, row, column):
    for error in errors:
      self._error(row, column, error)
      
  def _get_column_index(self, column_name):
    return self.sheet.columns.get_loc(column_name)

  def _info(self, row, column, message):
     self.managers.logger.info(self._format(row + 1, column + 1, message))
     
  def _general_info(self, message):
     self.managers.logger.info(self._format(None, None, message))
     
  def _error(self, row, column, message):
    try:
      self.managers.errors.add(self.sheet_name, row + 1, column + 1, message)
    except Exception as e:
      self.managers.errors.add(self.sheet_name, None, None, f"{e}\n{traceback.format_exc()}", self.managers.errors.WARNING)

  def _general_error(self, message):
    self.managers.errors.add(self.sheet_name, None, None, message)

  def _warning(self, row, column, message):
    self.managers.errors.add(self.sheet_name, row + 1, column + 1, message, self.managers.errors.WARNING)

  def _general_warning(self, message):
    self.managers.errors.add(self.sheet_name, None, None, message, self.managers.errors.WARNING)

  def _debug(self, row, column, message):
    self.managers.errors.add(self.sheet_name, row + 1, column + 1, message, self.managers.errors.DEBUG)

  def _general_debug(self, message):
    self.managers.errors.add(self.sheet_name, None, None, message, self.managers.errors.DEBUG)

  def _traceback(self, message):
    self.managers.logger.error(message)

  def _format(self, row, column, message):
    if self.sheet_name == None:
      return f"{self.message}"
    elif row == None:
      return f"In sheet {self.sheet_name}: {message}"
    else:
      return f"In sheet {self.sheet_name} at [{row},{column}]: {message}"

  def _get_sheet_names(self, file_path):
    wb = load_workbook(file_path, read_only=True, keep_links=False)
    return wb.sheetnames

  def _sheet_present(self, file_path, sheet_name):
    sheet_names = self._get_sheet_names(file_path)
    return sheet_name in sheet_names

  def _check_cell_value(self, file_path, sheet_name, row, column, value):
    wb = load_workbook(file_path, read_only=True, keep_links=False)
    ws = wb[sheet_name]
    #print(f"CELL={ws.cell(row, column).value}")
    return str(ws.cell(row, column).value).upper() == value

  def _state_split(self, s):

    OUT = "out"
    IN_QUOTED = "in_quoted"
    OUT_QUOTED = "out_quoted"
    IN_NORMAL = "in_normal"
    ESC = "escape"

    state = OUT
    result = []
    current = []
    exit = ""
    for c in s:
      if state == OUT:
        current = []
        if c in ['"', "'"]:
          state = IN_QUOTED
          exit = c
        elif c.isspace():
          pass
        else:
          state = IN_NORMAL
          current.append(c)
      elif state == IN_QUOTED:
        if c == '\\':
          state = ESC
        elif c == exit:
          result.append("".join(current).strip())
          state = OUT_QUOTED
        else:
          current.append(c)
      elif state == OUT_QUOTED:
        if c == ',':
          state = OUT
        else:
          pass
      elif state == IN_NORMAL:
        if c == ',':
          result.append("".join(current).strip())
          state = OUT
        else:
          current.append(c)
      elif state == ESC:
        if c == exit:
          current.append(c)
          state = IN_QUOTED
        else:
          current.append('\\')
          current.append(c)
      else:
        raise BaseSheet.StateError

    if state == OUT or state == OUT_QUOTED:
      pass
    elif state == IN_NORMAL:
      result.append("".join(current).strip())
    else:
      raise BaseSheet.FormatError
    return result
