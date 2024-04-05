import traceback
import datetime
from usdm_model.governance_date import GovernanceDate
from usdm_model.geographic_scope import GeographicScope
from usdm_model.study_title import StudyTitle
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.alias import Alias
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.iso_3166 import ISO3166
from usdm_excel.option_manager import Options
from usdm_excel.managers import Managers

class StudySheet(BaseSheet):

  SHEET_NAME = 'study'
  
  NAME_TITLE = 'name'
  TITLE_TITLE = 'studyTitle'
  VERSION_TITLE = 'studyVersion'
  TYPE_TITLE = 'studyType'
  PHASE_TITLE = 'studyPhase'
  ACRONYM_TITLE = 'studyAcronym'
  RATIONALE_TITLE = 'studyRationale'
  TA_TITLE = 'businessTherapeuticAreas'
  BRIEF_TITLE_TITLE = 'briefTitle'
  OFFICAL_TITLE_TITLE = 'officialTitle'
  PUBLIC_TITLE_TITLE = 'publicTitle'
  SCIENTIFIC_TITLE_TITLE = 'scientificTitle'
  PROTOCOL_VERSION_TITLE = 'protocolVersion'
  PROTOCOL_STATUS_TITLE = 'protocolStatus'

  DATES_HEADER_ROW = 15
  DATES_DATA_ROW = 16
  
  PARAMS_NAME_COL = 0
  PARAMS_DATA_COL = 1

  STUDY_VERSION_DATE = 'study_version'
  PROTOCOL_VERSION_DATE = 'protocol_document'

  def __init__(self, file_path: str, managers: Managers):
    try:
      super().__init__(file_path=file_path, managers=managers, sheet_name=self.SHEET_NAME, header=None)
      self.date_categories = [self.STUDY_VERSION_DATE, self.PROTOCOL_VERSION_DATE]
      self.phase = None
      self.version = None
      self.type = None
      self.name = None
      self.brief_title = None
      self.official_title = None
      self.public_title = None
      self.scientific_title = None
      self.protocol_version = None
      self.protocol_status = None
      self.title = None
      self.titles = []
      self.acronym = None
      self.rationale = None
      self.study = None
      self.study_version = None
      self.protocol_document_version = None
      self.therapeutic_areas = []
      self.timelines = {}
      self.dates = {}
      for category in self.date_categories:
        self.dates[category] = []
      self._process_sheet()
    except Exception as e:
      self._general_sheet_exception(e)

  def _process_sheet(self):
    fields = ['category', 'name', 'description', 'label', 'type', 'date', 'scopes']    
    for rindex, row in self.sheet.iterrows():
      field_name = self.read_cell(rindex, self.PARAMS_NAME_COL)
      if field_name == self.NAME_TITLE:
        self.name = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.TITLE_TITLE:
        if self.managers.option_manager.get(Options.USDM_VERSION) == '2':
          self.title = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.VERSION_TITLE:
        self.version = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.TYPE_TITLE:
        self.type = self.read_cdisc_klass_attribute_cell('Study', 'studyType', rindex, self.PARAMS_DATA_COL)
      elif field_name == self.PHASE_TITLE:
        phase = self.read_cdisc_klass_attribute_cell('Study', 'studyPhase', rindex, self.PARAMS_DATA_COL)
        self.phase = Alias(self.managers).code(phase, [])
      elif field_name == self.ACRONYM_TITLE:
        self.acronym = self._set_title(rindex, self.PARAMS_DATA_COL, "Study Acronym")
      elif field_name == self.RATIONALE_TITLE:
        self.rationale = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.TA_TITLE:
        self.therapeutic_areas = self.read_other_code_cell_mutiple(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.BRIEF_TITLE_TITLE:
        self.brief_title = self._set_title(rindex, self.PARAMS_DATA_COL, "Brief Study Title")
      elif field_name == self.OFFICAL_TITLE_TITLE:
        self.official_title = self._set_title(rindex, self.PARAMS_DATA_COL, "Official Study Title")
      elif field_name == self.PUBLIC_TITLE_TITLE:
        self.public_title = self._set_title(rindex, self.PARAMS_DATA_COL, "Public Study Title")
      elif field_name == self.SCIENTIFIC_TITLE_TITLE:
        self.scientific_title = self._set_title(rindex, self.PARAMS_DATA_COL, "Scientific Study Title")
      elif field_name == self.PROTOCOL_VERSION_TITLE:
        self.protocol_version = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.PROTOCOL_STATUS_TITLE:
        self.protocol_status = self.read_cdisc_klass_attribute_cell('StudyProtocolVersion', 'protocolStatus', rindex, self.PARAMS_DATA_COL) 
      elif rindex >= self.DATES_DATA_ROW:
        record = {}
        for cindex in range(0, len(self.sheet.columns)):
          field = fields[cindex]
          if field == 'category':
            cell = self.read_cell(rindex, cindex)
            if cell.lower() in self.date_categories:
              category = cell.lower()
            else:
              categories = ', '.join(f'"{w}"' for w in self.date_categories)
              self._error(rindex, cindex, f"Date category not recognized, should be one of {categories}, defaults to '{self.date_categories[0]}'")
              category = self.date_categories[0]
          elif field == 'type':
            record[field] = self.read_cdisc_klass_attribute_cell('GovernanceDate', 'type', rindex, cindex)
          elif field == 'date':
            cell = self.read_cell(rindex, cindex)
            record[field] = datetime.datetime.strptime(cell, '%Y-%m-%d %H:%M:%S')
          elif field == 'scopes':
            record[field] = self._read_scope_cell(rindex, cindex)
          else:
            cell = self.read_cell(rindex, cindex)
            record[field] = cell
        try:
          scopes = []
          for scope in record['scopes']:
            scope = GeographicScope(
              id=self.managers.id_manager.build_id(GeographicScope), 
              type=scope['type'], 
              code=scope['code']
            )
            scopes.append(scope)
        except Exception as e:
          self._general_error(f"Failed to create GeographicScope object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        try:
          date = GovernanceDate(
            id=self.managers.id_manager.build_id(GovernanceDate),
            name=record['name'],
            label=record['label'],
            description=record['description'],
            type=record['type'],
            dateValue=record['date'],
            geographicScopes=scopes
          )
          self.dates[category].append(date)
          self.managers.cross_references.add(record['name'], date)
        except Exception as e:
          self._general_error(f"Failed to create GovernanceDate object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")

  def _read_scope_cell(self, row_index, col_index):
    result = []
    value = self.read_cell(row_index, col_index)
    if value.strip() == "":
      self._error(row_index, col_index, "Empty cell detected where multiple geographic scope CT values expected")
      return result
    else:
      for item in self._state_split(value):
        if item.upper().strip() == "GLOBAL":
          # If we ever find global just return the one code
          return [{'type': CDISCCT(self.managers).code_for_attribute('GeographicScope', 'type', 'Global'), 'code': None}]
        else: 
          code = None
          if item.strip():
            outer_parts = item.split(":")
            if len(outer_parts) == 2:
              system = outer_parts[0].strip()
              value = outer_parts[1].strip()
              if system.upper() == "REGION":
                pt = 'Region'
                code = ISO3166().region_code(value)
              elif system.upper() == "COUNTRY":
                pt = 'Country'
                code = ISO3166(self.managers).code(value)
              else:
                self._error(row_index, col_index, f"Failed to decode geographic scope data {outer_parts}, must be either Global, Region using UN M49 codes, or Country using ISO3166 codes")
            else:
              self._error(row_index, col_index, f"Failed to decode geographic scope data {outer_parts}, no ':' detected")
          else:
            self._error(row_index, col_index, f"Failed to decode geographic scope data {item}, appears empty")
          if code:
            result.append({'type': CDISCCT(self.managers).code_for_attribute('GeographicScope', 'type', pt), 'code':  Alias.code(code, [])})
      return result

  def _set_title(self, rindex, cindex, title_type):
    if self.managers.option_manager.get(Options.USDM_VERSION) == '2':
      return self.read_cell(rindex, cindex)
    else:
      try:
        text = self.read_cell(rindex, cindex)
        if text:
          code = CDISCCT(self.managers).code_for_attribute('StudyVersion', 'titles', title_type)
          title = StudyTitle(id=self.managers.id_manager.build_id(StudyTitle), text=text, type=code)
          self.titles.append(title)
          self.managers.cross_references.add(title.id, title)
          return title
        else:
          return None
      except Exception as e:
        self._error(rindex, cindex, "Failed to create StudyTitle object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")
        