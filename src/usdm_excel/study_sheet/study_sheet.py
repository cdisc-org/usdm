from pydantic import BaseModel
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_identifiers_sheet.study_identifiers_sheet import StudyIdentifiersSheet
from usdm_excel.study_design_sheet.study_design_sheet import StudyDesignSheet
from usdm_excel.study_soa_sheet.study_soa_sheet import StudySoASheet
from usdm_excel.study_soa_v2_sheet.study_soa_v2_sheet import StudySoAV2Sheet
from usdm_excel.study_design_ii_sheet.study_design_ii_sheet import StudyDesignIISheet
from usdm_excel.study_design_population_sheet.study_design_population_sheet import StudyDesignPopulationSheet
from usdm_excel.study_design_objective_endpoint_sheet.study_design_objective_endpoint_sheet import StudyDesignObjectiveEndpointSheet
from usdm_excel.study_design_estimands_sheet.study_design_estimands_sheet import StudyDesignEstimandsSheet
from usdm_excel.study_design_procedure_sheet.study_design_procedure_sheet import StudyDesignProcedureSheet
from usdm_excel.study_design_encounter_sheet.study_design_encounter_sheet import StudyDesignEncounterSheet
from usdm_excel.study_design_element_sheet.study_design_element_sheet import StudyDesignElementSheet
from usdm_excel.study_design_arm_sheet.study_design_arm_sheet import StudyDesignArmSheet
from usdm_excel.study_design_epoch_sheet.study_design_epoch_sheet import StudyDesignEpochSheet
from usdm_excel.study_design_activity_sheet.study_design_activity_sheet import StudyDesignActivitySheet
from usdm_excel.study_design_timing_sheet.study_design_timing_sheet import StudyDesignTimingSheet
from usdm_excel.study_design_content_sheet.study_design_content_sheet import StudyDesignContentSheet
from usdm_excel.study_design_amendment_sheet.study_design_amendment_sheet import StudyDesignAmendmentSheet
from usdm_excel.alias import Alias
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.option_manager import *
from usdm_model.study import Study
from usdm_model.study_version import StudyVersion
from usdm_model.study_protocol_document_version import StudyProtocolDocumentVersion
from usdm_model.study_protocol_document import StudyProtocolDocument
from usdm_model.wrapper import Wrapper
from usdm_model.governance_date import GovernanceDate
from usdm_model.geographic_scope import GeographicScope
from usdm_excel.narrative_content import NarrativeContent
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.iso_3166 import ISO3166
import traceback
import datetime

class StudySheet(BaseSheet):

  NAME_ROW = 0
  TITLE_ROW = 1
  VERSION_ROW = 2
  TYPE_ROW = 3
  PHASE_ROW = 4
  ACRONYM_ROW = 5
  RATIONALE_ROW = 6
  TA_ROW = 7
  BRIEF_TITLE_ROW = 8
  OFFICAL_TITLE_ROW = 9
  PUBLIC_TITLE_ROW = 10
  SCIENTIFIC_TITLE_ROW = 11
  PROTOCOL_VERSION_ROW = 12
  PROTOCOL_STATUS_ROW = 13

  DATES_HEADER_ROW = 15
  DATES_DATA_ROW = 16
  
  PARAMS_DATA_COL = 1

  STUDY_VERSION_DATE = 'study_version'
  PROTOCOL_VERSION_DATE = 'protocol_document'

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='study', header=None)
      self.date_categories = [self.STUDY_VERSION_DATE, self.PROTOCOL_VERSION_DATE]
      self.soa_version = None
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
      self.study_amendments = StudyDesignAmendmentSheet(file_path)
      self.study_identifiers = StudyIdentifiersSheet(file_path)
      self.procedures = StudyDesignProcedureSheet(file_path)
      self.encounters = StudyDesignEncounterSheet(file_path)
      self.elements = StudyDesignElementSheet(file_path)
      self.arms = StudyDesignArmSheet(file_path)
      self.epochs = StudyDesignEpochSheet(file_path)
      self.timings = StudyDesignTimingSheet(file_path)
      self.activities = StudyDesignActivitySheet(file_path)
      self.study_design = StudyDesignSheet(file_path)
      self._process_soa(file_path)
      self.ii = StudyDesignIISheet(file_path)
      self.study_populations = StudyDesignPopulationSheet(file_path)
      self.oe = StudyDesignObjectiveEndpointSheet(file_path)
      self.estimands = StudyDesignEstimandsSheet(file_path)
      self.contents = StudyDesignContentSheet(file_path)
      #self.protocols[-1].contents = self.contents.items

      study_design = self.study_design.study_designs[0]
      study_design.studyScheduleTimelines.append(self.soa.timeline)
      study_design.encounters = self.encounters.items
      study_design.activities = self.soa.activities
      activity_ids = [item.id for item in study_design.activities]
      study_design.biomedicalConcepts = self.soa.biomedical_concepts
      study_design.bcSurrogates = self.soa.biomedical_concept_surrogates
      for key,tl in self.timelines.items():
        study_design.studyScheduleTimelines.append(tl.timeline)
        for activity in tl.activities:
          if activity.id not in activity_ids:
            study_design.activities.append(activity)
            activity_ids.append(activity.id)
        study_design.biomedicalConcepts += tl.biomedical_concepts
        study_design.bcSurrogates += tl.biomedical_concept_surrogates
      study_design.studyIndications = self.ii.indications
      study_design.studyInvestigationalInterventions = self.ii.interventions
      study_design.studyPopulations = self.study_populations.populations
      study_design.studyObjectives = self.oe.objectives
      study_design.studyEstimands = self.estimands.estimands
      #study_design.contents = self.contents.items

      try:
        #print(f"DATES SPDV: {self.dates[self.PROTOCOL_VERSION_DATE]}")
        self.protocol_document_version = StudyProtocolDocumentVersion(
          id=id_manager.build_id(StudyProtocolDocumentVersion), 
          briefTitle=self.brief_title,
          officialTitle=self.official_title,
          publicTitle=self.public_title,
          scientificTitle=self.scientific_title,
          protocolVersion=self.protocol_version,
          protocolStatus=self.protocol_status,
          dateValues=self.dates[self.PROTOCOL_VERSION_DATE]
          )
        self.protocol_document_version.contents = self.contents.items
        cross_references.add(self.protocol_document_version.id, self.protocol_document_version)
      except Exception as e:
        self._general_error(f"Failed to create StudyProtocolDocumentVersion object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")

      try:
        study_protocol_document = StudyProtocolDocument(
          id=id_manager.build_id(StudyProtocolDocument), 
          name=f"Protocol_Document_{self.name}", 
          versions=[self.protocol_document_version])
      except Exception as e:
        self._general_error(f"Failed to create StudyProtocolDocument object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")

      try:
        #f"DATES SV: {self.dates[self.STUDY_VERSION_DATE]}")
        self.study_version = StudyVersion(
          id=id_manager.build_id(StudyVersion),
          studyTitle=self.title,
          studyVersion=self.version,
          type=self.type,
          studyPhase=self.phase,
          businessTherapeuticAreas=self.therapeutic_areas,
          studyRationale=self.rationale,
          studyAcronym=self.acronym,
          studyIdentifiers=self.study_identifiers.identifiers,
          documentVersionId=self.protocol_document_version.id,
          studyDesigns=self.study_design.study_designs,
          dateValues=self.dates[self.STUDY_VERSION_DATE],
          amendments=self.study_amendments.items
        )
      except Exception as e:
        self._general_error(f"Failed to create StudyVersion object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")

      try:
        self.study = Study(
          id=None, # No Id, will be allocated a UUID
          name=f"Study_{self.name}", 
          versions=[self.study_version],
          documentedBy=study_protocol_document
        )
        cross_references.add("STUDY", self.study)
      except Exception as e:
        self._general_error(f"Failed to create Study object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")

    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def study_sponsor(self):
    return self.cdisc_code(code="C93453", decode="Study Registry")

  def study_regulatory(self):
    return self.cdisc_code(code="C93453", decode="Study Registry")

  def the_study(self):
    return self.study
  
  def api_root(self):
    return Wrapper(study=self.study)

  def to_html(self):
    return NarrativeContent(self.title, self.study.versions[0].documentVersion).to_html()

  def to_pdf(self):
    return NarrativeContent(self.title, self.study.versions[0].documentVersion).to_pdf()

  def _process_sheet(self):
    fields = ['category', 'name', 'description', 'label', 'type', 'date', 'scopes']    
    for rindex, row in self.sheet.iterrows():
      if rindex == self.NAME_ROW:
        self.name = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.TITLE_ROW:
        self.title = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.VERSION_ROW:
        self.version = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.TYPE_ROW:
        self.type = self.read_cdisc_klass_attribute_cell('Study', 'studyType', rindex, self.PARAMS_DATA_COL)
      elif rindex == self.PHASE_ROW:
        phase = self.read_cdisc_klass_attribute_cell('Study', 'studyPhase', rindex, self.PARAMS_DATA_COL)
        self.phase = Alias().code(phase, [])
      elif rindex == self.ACRONYM_ROW:
        self.acronym = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.RATIONALE_ROW:
        self.rationale = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.TA_ROW:
        self.therapeutic_areas = self.read_other_code_cell_mutiple(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.BRIEF_TITLE_ROW:
        self.brief_title = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.OFFICAL_TITLE_ROW:
        self.official_title = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.PUBLIC_TITLE_ROW:
        self.public_title = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.SCIENTIFIC_TITLE_ROW:
        self.scientific_title = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.PROTOCOL_VERSION_ROW:
        self.protocol_version = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.PROTOCOL_STATUS_ROW:
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
            #print(f"TYPE: {record[field]}") 
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
              id=id_manager.build_id(GeographicScope), 
              type=scope['type'], 
              code=scope['code']
            )
            scopes.append(scope)
            #print(f"SCOPE: {scope}")
        except Exception as e:
          self._general_error(f"Failed to create GeographicScope object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
          #print(f"SCOPE: {traceback.format_exc()}")
        try:
          date = GovernanceDate(
            id=id_manager.build_id(GovernanceDate),
            name=record['name'],
            label=record['label'],
            description=record['description'],
            type=record['type'],
            dataValue=record['date'],
            geographicScopes=scopes
          )
          self.dates[category].append(date)
          #print(f"DATE: {date}")
        except Exception as e:
          self._general_error(f"Failed to create GovernanceDate object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
          #print(f"DATE: {traceback.format_exc()}")

  def _process_soa(self, file_path):
    for timeline in self.study_design.other_timelines:
      tl = self._process_timeline(file_path, timeline)
      self.timelines[timeline] = tl
      cross_references.add(timeline, tl.timeline)
    self.soa = self._process_timeline(file_path, self.study_design.main_timeline, True)

  def _process_timeline(self, file_path, timeline, main_timeline=False):
    if not self.soa_version:
      self._general_info("Detecting SoA sheet version ...")
      tl = StudySoASheet(file_path, timeline, main=main_timeline, require={'row': 1, 'column': 3, 'value': 'EPOCH'})
      if tl.success:
        self._general_info("SoA sheet version 1 detected")
        self.soa_version = 1 
      else:
        self._general_info("SoA sheet version 2 detected")
        self.soa_version = 2
        tl = StudySoAV2Sheet(file_path, timeline, main=main_timeline)
        #print("---- SoA Timing ----")
        tl.set_timing_references(self.timings.items)
    elif self.soa_version == 1:
      self._general_info("Set to SoA sheet version 1")
      tl = StudySoASheet(file_path, timeline, main=main_timeline)
    else:
      self._general_info("Set to SoA sheet version 2")
      tl = StudySoAV2Sheet(file_path, timeline, main=main_timeline)
      #print("---- SoA Timing ----")
      tl.set_timing_references(self.timings.items)
    return tl

  def _read_scope_cell(self, row_index, col_index):
    result = []
    value = self.read_cell(row_index, col_index)
    if value.strip() == "":
      self._error(row_index, col_index, "Empty cell detected where multiple geographic scope CT values expected")
      return result
    else:
      for item in self._state_split(value):
        #print(f"SCOPE ITEM: {item}")
        if item.upper().strip() == "GLOBAL":
          # If we ever find global just return the one code
          return [{'type': CDISCCT().code_for_attribute('GeographicScope', 'type', 'Global'), 'code': None}]
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
                code = ISO3166().code(value)
              else:
                self._error(row_index, col_index, f"Failed to decode geographic scope data {outer_parts}, must be either Global, Region using UN M49 codes, or Country using ISO3166 codes")
            else:
              self._error(row_index, col_index, f"Failed to decode geographic scope data {outer_parts}, no ':' detected")
          else:
            self._error(row_index, col_index, f"Failed to decode geographic scope data {item}, appears empty")
          if code:
            result.append({'type': CDISCCT().code_for_attribute('GeographicScope', 'type', pt), 'code':  Alias().code(code, [])})
      return result
