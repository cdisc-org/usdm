import pandas as pd
from usdm_excel.id_manager import id_manager
from usdm_excel.cdisc_ct import CDISCCT
from usdm_model.code import Code
from usdm_excel.ct_version_manager import ct_version_manager
from usdm_excel.errors.errors import error_manager
from usdm_excel.logger import package_logger

class BaseSheet():

  def __init__(self, file_path, sheet_name, header=0):
    self.file_path = file_path
    self.sheet_name = sheet_name
    self.sheet = pd.read_excel(open(file_path, 'rb'), sheet_name=sheet_name, header=header)
    package_logger.info("Reading sheet %s" % (sheet_name))
    
  def read_cell_by_name(self, row_index, field_name):
    try:
      col_index = self.sheet.columns.get_loc(field_name)
      return self.read_cell(row_index, col_index)
    except Exception as e:
      self.error(row_index + 1, col_index, "Error (%s) reading cell row '%s', field '%s'" % (e, row_index, field_name))
      return ""

  def read_cell(self, row_index, col_index):
    try:
      if pd.isnull(self.sheet.iloc[row_index, col_index]):
        return ""
      else:
        return str(self.sheet.iloc[row_index, col_index]).strip()
    except Exception as e:
      self.error(row_index + 1, col_index, "Error (%s) reading cell row '%s', field '%s'" % (e, row_index, col_index))
      return ""

  def read_cell_multiple(self, rindex, cindex):
    results = []
    value = self.read_cell(rindex, cindex)
    if value.strip() == '':
      return results
    for part in value.split(","):
      results.append(part.strip())
    return results

  #@DeprecationWarning
  def clean_cell(self, row, index, field_name):
    try:
      if pd.isnull(row[field_name]):
        return ""
      else:
        return str(row[field_name]).strip()
    except Exception as e:
      col = self.sheet.columns.get_loc(field_name)
      self.error(index + 1, col, "Cell error '%s'" % (e))
      return ""

  #@DeprecationWarning
  def clean_cell_unnamed(self, rindex, cindex):
    try:
      if pd.isnull(self.sheet.iloc[rindex, cindex]):
        return ""
      else:
        return str(self.sheet.iloc[rindex, cindex]).strip()
    except Exception as e:
      self.error(rindex + 1, cindex + 1, "Cell error '%s'" % (e))
      return ""

  #@DeprecationWarning
  def clean_cell_unnamed_multiple(self, rindex, cindex):
    results = []
    value = self.clean_cell_unnamed(rindex, cindex)
    if value.strip() == '':
      return results
    for part in value.split(","):
      results.append(part.strip())
    return results

  # def clean_cell_unnamed_new(self, rindex, cindex):
  #   try:
  #     if pd.isnull(self.sheet.iloc[rindex, cindex]):
  #       return "", True
  #     else:
  #       return self.sheet.iloc[rindex, cindex].strip(), False
  #   except Exception as e:
  #     self.error(rindex + 1, cindex + 1, "Cell error '%s'" % (e))
  #     return "", True

  def read_cell_with_previous(self, row_index, col_index, first_col_index):
    try:
      i = col_index
      while i >= first_col_index:
        if pd.isnull(self.sheet.iloc[row_index, i]):
          i -= 1
        else:
          return self.sheet.iloc[row_index, i].strip()
      self.error(row_index + 1, col_index + 1, "Blank cell error")
      return ""
    except Exception as e:
      self.error(row_index + 1, col_index, "Error (%s) reading cell row '%s', field '%s'" % (e, row_index, col_index))
      return ""

  def read_boolean_cell(self, value):
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
      self.error(0, 0, "CDISC code error '%s'" % (e))
      return None

  def read_other_code_cell_by_name(self, row_index, field_name):
    col_index = self.sheet.columns.get_loc(field_name)
    return self.read_other_code_cell(row_index, col_index)

  def read_other_code_cell(self, row_index, col_index):
    value = self.read_cell(row_index, col_index)
    if value.strip() == "":
      return None
    return self.decode_other_code(value)

  def decode_other_code(self, value):
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
        self.error(0, 0, "Other code error for data '%s', no '=' detected" % (value))
    else:
      self.error(0, 0, "Other code error for data '%s', no ':' detected" % (value))
    return None
  
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
      code = self.decode_other_code(item.strip())
      if not code == None:
        result.append(code)
    return result

  def cdisc_klass_attribute_cell(self, klass, attribute, value):
    return CDISCCT().code_for_attribute(klass, attribute, value)

  def cdisc_klass_attribute_cell_multiple(self, klass, attribute, value):
    result = []
    items = value.split(",")
    for item in items:
      code =  CDISCCT().code_for_attribute(klass, attribute, item.strip())
      if not code == None:
        result.append(code)
    return result

  def double_link(self, items, id, prev, next):
    for idx, item in enumerate(items):
      if idx == 0:
        setattr(item, prev, None)
      else:
        the_id = getattr(items[idx-1], id)
        setattr(item, prev, the_id)
      if idx == len(items)-1:  
        setattr(item, next, None)
      else:
        the_id = getattr(items[idx+1], id)
        setattr(item, next, the_id)

  def error(self, row, column, message):
    error_manager.add("Needed", row, column, message)
