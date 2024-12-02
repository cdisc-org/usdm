import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.study_amendment import StudyAmendment
from usdm_model.study_amendment_reason import StudyAmendmentReason
from usdm_model.geographic_scope import GeographicScope
from usdm_model.subject_enrollment import SubjectEnrollment
from usdm_model.quantity import Quantity
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.iso_3166 import ISO3166
from usdm_excel.alias import Alias
from usdm_excel.quantity_type import QuantityType
from usdm_excel.globals import Globals

class StudyAmendmentSheet(BaseSheet):

  SHEET_NAME = 'studyAmendments'
  
  def __init__(self, file_path: str, globals: Globals):
    try:
      self.items = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME, optional=True)
      if self.success:
        for index, row in self.sheet.iterrows():
          secondaries = []
          number = self.read_cell_by_name(index, 'number')
          summary = self.read_cell_by_name(index, 'summary')
          #substantial = self.read_boolean_cell_by_name(index, 'substantialImpact')
          notes = self.read_cell_multiple_by_name(index, 'notes', must_be_present=False)
          primary_reason = self._read_primary_reason_cell(index)
          primary = self._amendment_reason(primary_reason)
          secondary_reasons = self._read_secondary_reason_cell(index)
          for reason in secondary_reasons:
            amendment_reason = self._amendment_reason(reason)        
            if amendment_reason:
              secondaries.append(amendment_reason)
          enrollments = self._read_enrollment_cell(index)
          scopes = self._read_geographic_scopes_cell(index)
          params = {
            'number': number,
            'summary': summary,
            #'substantialImpact': substantial,
            'primaryReason': primary,
            'secondaryReasons': secondaries,
            'enrollments': enrollments,
            'geographicScopes': scopes
          }
          item = self.create_object(StudyAmendment, params)
          if item:
            self.items.append(item)
            self.globals.cross_references.add(item.number, item)
            self.add_notes(item, notes)
        self.items.sort(key=lambda d: int(d.number))
        self.previous_link(self.items, 'previousId')
        
    except Exception as e:
      self._sheet_exception(e)

  def _amendment_reason(self, reason):
    item = self.create_object(StudyAmendmentReason, {'code': reason['code'], 'otherReason': reason['other']})
    return item
    
  def _read_enrollment_cell(self, row_index):
    result = []
    col_index = self.sheet.columns.get_loc('enrollment')
    value = self.read_cell(row_index, col_index)
    if value.strip() == '':
      self._error(row_index, col_index, "Empty cell detected where enrollment values expected")
    else:
      for item in self._state_split(value):
        key_value = self._key_value(item, row_index, col_index)
        if key_value[0] == "COHORT":
          pass
        elif key_value[0] == "SITE":
          pass
        elif key_value[0] == "GLOBAL":
          quantity = self._get_quantity(key_value[1])
          scope = self._scope('Global', None)
          result.append(self._enrollment(quantity, scope=scope))
        elif key_value[0] == "REGION": 
          code, quantity = self._country_region_quantity(key_value[1], 'Region', row_index, col_index)
          if code:
            scope = self._scope('Region', code)
            result.append(self._enrollment(quantity, scope=scope))
        elif key_value[0] == "COUNTRY": 
          code, quantity = self._country_region_quantity(key_value[1], 'Country', row_index, col_index)
          if code:
            scope = self._scope('Country', code)
            result.append(self._enrollment(quantity, scope=scope))
    return result

  def _read_geographic_scopes_cell(self, row_index):
    result = []
    col_index = self.sheet.columns.get_loc('geographicScope')
    value = self.read_cell(row_index, col_index, default='')
    if value.strip() == '':
      self._warning(row_index, col_index, "Empty cell detected where geographic scope values expected, assuming global scope.")
      result.append(self._scope('Global', None))
    else:
      for item in self._state_split(value):
        key_value = self._key_value(item, row_index, col_index, allow_single=True)
        if key_value[0] == "GLOBAL":
          result.append(self._scope('Global', None))
        elif key_value[0] == "REGION": 
          code = self._country_region(key_value[1], 'Region')
          if code:
            scope = self._scope('Region', code)
            result.append(scope)
        elif key_value[0] == "COUNTRY": 
          code = self._country_region(key_value[1], 'Country')
          if code:
            scope = self._scope('Country', code)
            result.append(scope)
    return result

  def _scope(self, type, code):
    scope_type = CDISCCT(self.globals).code_for_attribute('GeographicScope', 'type', type)
    alias = Alias(self.globals).code(code, []) if code else None
    return self.create_object(GeographicScope, {'type': scope_type, 'code': alias})

  def _enrollment(self, quantity, **kwargs):
    applies_to = None
    applies_to_id = None
    if 'scope' in kwargs:
      applies_to = kwargs['scope']
    if 'cohort' in kwargs:
      applies_to_id = kwargs['cohort']
    if 'site' in kwargs:
      applies_to_id = kwargs['site']
    return self.create_object(SubjectEnrollment, {'name': "XXX", 'quantity': quantity, 'appliesTo': applies_to, 'appliesToId': applies_to_id})

  def _key_value(self, text: str, row_index: int, col_index: int, allow_single=False):
    if text.strip():
      parts = text.split(":")
      if len(parts) == 2:
        return [parts[0].strip().upper(), parts[1].strip()]
      elif len(parts) == 1 and allow_single:
        return [parts[0].strip().upper(), '']
    self._error(row_index, col_index, f"Failed to decode geographic enrollment data '{text}', incorrect format, missing ':'?")
    return ['', '']

  def _country_region_quantity(self, text: str, type: str, row_index: int, col_index: int):
    name_value = text.split('=')
    if len(name_value) == 2:
      quantity = self._get_quantity(name_value[1].strip())
      code = self._country_region(name_value[0].strip(), type)
      return code, quantity
    else:
      self._error(row_index, col_index, f"Failed to decode geographic enrollment data '{text}', incorrect format, missing '='?")
      return None, None

  def _country_region(self, text: str, type: str):
    return ISO3166(self.globals).region_code(text) if type == 'Region' else ISO3166(self.globals).code(text)

  def _get_quantity(self, text):
    quantity = QuantityType(text, self.globals, True, False)
    unit = Alias(self.globals).code(quantity.units_code, [])
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
        return {'code': CDISCCT(self.globals).code_for_attribute('StudyAmendmentReason', 'code', 'Other'), 'other': parts[1].strip()}
      else:
        self._error(row_index, col_index, f"Failed to decode reason data {text}, no '=' detected")
    else:
      code = CDISCCT(self.globals).code_for_attribute('StudyAmendmentReason', 'code', value)
      if code is None:
        self._error(row_index, col_index, f"CDISC CT not found for value '{value}'.")
      return {'code': code, 'other': None}