import pandas as pd
from usdm_excel.id_manager import id_manager
from usdm_excel.cdisc_ct import CDISCCT
from usdm.code import Code
from usdm_excel.ct_version_manager import ct_version_manager

class BaseSheet():

  def __init__(self, sheet):
    self.sheet = sheet

  def clean_cell(self, row, index, field_name):
    try:
      if pd.isnull(row[field_name]):
        return ""
      else:
        return str(row[field_name]).strip()
    except Exception as e:
      print("Clean cell error (%s) for field '%s' in row %s" % (e, field_name, index + 1))
      return ""

  def clean_cell_unnamed(self, rindex, cindex):
    try:
      if pd.isnull(self.sheet.iloc[rindex, cindex]):
        return ""
      else:
        return str(self.sheet.iloc[rindex, cindex]).strip()
    except Exception as e:
      print("Clean cell unnamed error (%s) for cell [%s, %s]" % (e, rindex + 1, cindex + 1))
      return ""

  def clean_cell_unnamed_multiple(self, rindex, cindex):
    results = []
    value = self.clean_cell_unnamed(rindex, cindex)
    if value.strip() == '':
      return results
    for part in value.split(","):
      results.append(part.strip())
    return results

  def clean_cell_unnamed_new(self, rindex, cindex):
    try:
      if pd.isnull(self.sheet.iloc[rindex, cindex]):
        return "", True
      else:
        return self.sheet.iloc[rindex, cindex].strip(), False
    except Exception as e:
      print("Clean cell unnamed error (%s) for cell [%s, %s]" % (e, rindex + 1, cindex + 1))
      return "", True

  def clean_cell_unnamed_with_previous(self, rindex, cindex, first_cindex):
    try:
      i = cindex
      while i >= first_cindex:
        if pd.isnull(self.sheet.iloc[rindex, i]):
          i -= 1
        else:
          return self.sheet.iloc[rindex, i].strip(), False
      print("Clean cell unnamed with previous is blank for cell [%s, %s]" % (rindex + 1, cindex + 1))
      return "", True
    except Exception as e:
      print("Clean cell unnamed with previous error (%s) for cell [%s, %s]" % (e, rindex + 1, cindex + 1))
      return "", True

  def boolean_cell(self, value):
    if value.strip().upper() in ['Y', 'YES', 'TRUE', '1']:
      return True
    return False

  def cdisc_code_cell(self, value):
    if value.strip() == "":
      return None
    parts = value.split("=")
    try:
      return CDISCCT().code(code=parts[0].strip(), decode=parts[1].strip())
    except Exception as e:
      print("CDISC code error (%s) for data %s" % (e, value))
      return None

  def other_code_cell(self, value):
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
        print("Other code error for data '%s', no '=' detected" % (value))
    else:
      print("Other code error for data '%s', no ':' detected" % (value))
    return None
  
  def other_code_cell_mutiple(self, value):
    result = []
    if value.strip() == '':
      return result
    items = value.split(",")
    for item in items:
      code = self.other_code_cell(item.strip())
      if not code == None:
        result.append(code)
    return result

  # def cdisc_code_set_cell(self, items):
  #   results = []
  #   parts = items.split(",")
  #   for part in parts:
  #     result = self.cdisc_code_cell(part.strip())
  #     if not result == None:
  #       results.append(result)
  #   return results

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