from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_model.study_amendment import StudyAmendment
from usdm_model.study_amendment_reason import StudyAmendmentReason
from usdm_model.geographic_scope import SubjectEnrollment
from usdm_model.quantity import Quantity
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.iso_3166 import ISO3166
from usdm_excel.alias import Alias
from usdm_excel.quantity_type import QuantityType

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
          summary = self.read_cell_by_name(index, 'summary')
          substantial = self.read_boolean_cell_by_name(index, 'substantialImpact')
          primary_reason = self._read_primary_reason_cell(index)
          primary = self._amendment_reason(primary_reason)
          #print(f"PRIMARY: {primary}")
          secondary_reasons = self._read_secondary_reason_cell(index)
          for reason in secondary_reasons:
            amendment_reason = self._amendment_reason(reason)        
            if amendment_reason:
              #print(f"SECONDARY: {amendment_reason}")
              secondaries.append(amendment_reason)
          enrollment = self._read_enrollment_cell(index)
          enrollments = self._enrollments(enrollment)
          #print(f"ENROLLMENT: {enrollment}")
          try:
            item = StudyAmendment(
              id=id_manager.build_id(StudyAmendment), 
              number=number,
              summary=summary,
              substantialImpact=substantial,
              primaryReason=primary,
              secondaryReasons=secondaries,
              enrollments=enrollments
            )
          except Exception as e:
            self._general_error(f"Failed to create StudyAmendment object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            self.items.append(item)
            cross_references.add(item.number, item)
        self.items.sort(key=lambda d: int(d.number))
        self.previous_link(self.items, 'previousId')
        
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def _enrollments(self, enrollments):
    results = []
    for enrollment in enrollments:
      try:
        #print(f"ENROLL: {enrollment}")
        item = SubjectEnrollment(
          id=id_manager.build_id(SubjectEnrollment),
          type=enrollment['type'],
          code=enrollment['code'],
          quantity=enrollment['quantity']
        )
      except Exception as e:
        self._general_error(f"Failed to create SubjectEnrollment object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")
        return None
      else:
        results.append(item)
    return results

  def _amendment_reason(self, reason):
    #print(f"AR1: {reason}")
    try:
      item = StudyAmendmentReason(
        id=id_manager.build_id(StudyAmendmentReason), 
        code=reason['code'],
        otherReason=reason['other']
      )
    except Exception as e:
      self._general_error(f"Failed to create StudyAmendmentReason object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      print(f"AR2: {traceback.format_exc()}")
      return None
    else:
      return item
    
  def _read_enrollment_cell(self, row_index):
    result = []
    col_index = self.sheet.columns.get_loc('enrollment')
    value = self.read_cell(row_index, col_index)
    #print(f"ENROL1: {value}")
    if value.strip() == "":
      self._error(row_index, col_index, "Empty cell detected where geographic enrollment values expected")
      return [{'type': CDISCCT().code_for_attribute('GeographicScope', 'type', 'Global'), 'code': None, 'quantity': '0'}]
    else:
      for item in self._state_split(value):
        #print(f"ENROL2: {item}")
        if item.strip().upper().startswith("GLOBAL"):
          # If we ever find global just return the one code
          text = item.strip()
          parts = text.split(":")
          if len(parts) == 2:
            quantity = self._get_quantitiy(parts[1].strip())
            return [{'type': CDISCCT().code_for_attribute('GeographicScope', 'type', 'Global'), 'code': None, 'quantity': quantity}]
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
                #quantity = name_value[1].strip()
                quantity = self._get_quantitiy(name_value[1].strip())
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

  def _get_quantitiy(self, text):
    #print(f"QUANTITY1: {text}")
    quantity = QuantityType(text, True, False)
    unit = Alias().code(quantity.units_code, []) if quantity.units_code else None
    #print(f"QUANTITY2: {quantity_details}")
    return self.create_object(Quantity, {'value': float(quantity.value), 'unit': unit})

  def _read_secondary_reason_cell(self, row_index):
    results = []
    col_index = self.sheet.columns.get_loc('secondaryReasons')
    value = self.read_cell(row_index, col_index)
    if not value.strip():
      return results
    parts = value.strip().split(',')
    for part in parts:
      result = self._extract_reason(part, row_index, col_index)
      if result:
        results.append(result)
    return results
      
  def _read_primary_reason_cell(self, row_index):
    col_index = self.sheet.columns.get_loc('primaryReason')
    value = self.read_cell(row_index, col_index)
    return self._extract_reason(value, row_index, col_index)
  
  def _extract_reason(self, value, row_index, col_index):
    if value.strip() == "":
      self._error(row_index, col_index, "Empty cell detected where CDISC CT value expected.")
      return None
    elif value.strip().upper().startswith('OTHER'):
      text = value.strip()
      parts = text.split("=")
      if len(parts) == 2:
        return {'code': CDISCCT().code_for_attribute('StudyAmendmentReason', 'code', 'Other'), 'other': parts[1].strip()}
      else:
        self._error(row_index, col_index, f"Failed to decode reason data {text}, no '=' detected")
    else:
      code = CDISCCT().code_for_attribute('StudyAmendmentReason', 'code', value)
      if code is None:
        self._error(row_index, col_index, f"CDISC CT not found for value '{value}'.")
      return {'code': code, 'other': None}