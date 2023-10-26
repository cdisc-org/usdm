from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_model.study_amendment import StudyAmendment
from usdm_model.study_amendment_reason import StudyAmendmentReason
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.iso_3166 import ISO3166
from usdm_excel.alias import Alias

import traceback

class StudyDesignAmendmentSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyAmendments', optional=True)
      self.items = []
      if self.success:
        for index, row in self.sheet.iterrows():
          secondaries = []
          number = self.read_cell_by_name(index, 'number')
          summary = self.read_description_by_name(index, 'summary')
          substantial = self.read_boolean_cell_by_name(index, 'substantialImpact')
          primary_reason = self._read_reason_cell('StudyAmendmentReason', 'code', index, 'primaryReason')
          secondary_reasons = self._read_reason_cell_multiple('StudyAmendmentReason', 'code', index, 'secondaryReason')
          enrollment = self._read_enrollment_cell(index)
          primary = self._amendment_reason(primary_reason)        
          for reason in secondary_reasons:
            amendment_reason = self._amendment_reason(reason)        
            if amendment_reason:
              secondaries.append(amendment_reason)
          try:
            item = StudyAmendment(
              id=id_manager.build_id(StudyAmendment), 
              number=number,
              summary=summary,
              substantialImpact=substantial,
              primaryReason=primary,
              secondaryReasons=secondaries,
              enrollments=enrollment
            )
            self.items.append(item)
          except Exception as e:
            self._general_error(f"Failed to create StudyAmendment object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            self.items.append(item)
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def _amendment_reason(self, reason):
    try:
      item = StudyAmendmentReason(
        id=id_manager.build_id(StudyAmendmentReason), 
        code=reason['code'],
        otherReason=reason['other']
      )
    except Exception as e:
      self._general_error(f"Failed to create StudyAmendmentReason object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      return None
    else:
      return item
    
  def _read_enrollment_cell(self, row_index, col_index):
    result = []
    value = self.read_cell(row_index, col_index)
    if value.strip() == "":
      self._error(row_index, col_index, "Empty cell detected where multiple geographic enrollment values expected")
      return result
    else:
      for item in self._state_split(value):
        #print(f"SCOPE ITEM: {item}")
        if item.strip().upper().startswith("GLOBAL"):
          # If we ever find global just return the one code
          text = item.strip()
          parts = text.split(":")
          if len(parts) == 2:
            return [{'type': CDISCCT().code_for_attribute('GeographicScope', 'type', 'Global'), 'code': None, 'quantity': parts[1].strip()}]
          else:
            self._error(row_index, col_index, f"Failed to decode enrollment data {item}, no '=' detected")
          return 
        else: 
          code = None
          if item.strip():
            outer_parts = item.split(":")
            if len(outer_parts) == 2:
              system = outer_parts[0].strip()
              value = outer_parts[1].strip()
              name_value = value.split('=')
              if len(name_value) == 2:
                quantity = name_value[1].strip()
                if system.upper() == "REGION":
                  pt = 'Region'
                  code = ISO3166().region_code(value)
                elif system.upper() == "COUNTRY":
                  pt = 'Country'
                  code = ISO3166().code(value)
                else:
                  self._error(row_index, col_index, f"Failed to decode geographic enrollment data {name_value}, must be either Region or Country using ISO3166 codes")
              else:
                self._error(row_index, col_index, f"Failed to decode geographic enrollment data {name_value}, no '=' detected")
            else:
              self._error(row_index, col_index, f"Failed to decode geographic enrollment data {outer_parts}, no ':' detected")
          else:
            self._error(row_index, col_index, f"Failed to decode geographic enrollment data {item}, appears empty")
          if code:
            result.append({'type': CDISCCT().code_for_attribute('GeographicScope', 'type', pt), 'code': Alias().code(code, []), 'quantity': quantity})
      return result


  def _read_reason_cell_multiple(self, klass, attribute, row_index, col_index):
    results = []
    value = self.read_cell(row_index, col_index)
    parts = value.strip().split(',')
    for part in parts:
      result = self._extract_reason(part, klass, attribute, row_index, col_index)
      if result:
        results.append(result)
    return results
      
  def _read_reason_cell(self, klass, attribute, row_index, col_index):
    value = self.read_cell(row_index, col_index)
    return self._extract_reason(value, klass, attribute, row_index, col_index)
  
  def _extract_reason(self, value, klass, attribute, row_index, col_index):
    if value.strip() == "":
      self._error(row_index, col_index, "Empty cell detected where CDISC CT value expected.")
      return None
    elif value.strip().upper().startswith('OTHER'):
      text = value.strip()
      parts = text.split("=")
      if len(parts) == 2:
        return {'code': None, 'other': parts[1].strip()}
      else:
        self._error(row_index, col_index, f"Failed to decode reason data {text}, no '=' detected")
    else:
      code = CDISCCT().code_for_attribute(klass, attribute, value)
      if code is None:
        self._error(row_index, col_index, f"CDISC CT not found for value '{value}'.")
      return {'code': code, 'other': None}