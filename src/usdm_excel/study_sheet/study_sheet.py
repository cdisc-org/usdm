from pydantic import BaseModel
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_identifiers_sheet.study_identifiers_sheet import StudyIdentifiersSheet
from usdm_excel.study_design_sheet.study_design_sheet import StudyDesignSheet
from usdm_excel.study_soa_sheet.study_soa_sheet import StudySoASheet
from usdm_excel.study_soa_v2_sheet.study_soa_v2_sheet import StudySoAV2Sheet
from usdm_excel.study_design_indication_sheet.study_design_indication_sheet import StudyDesignIndicationSheet
from usdm_excel.study_design_intervention_sheet.study_design_intervention_sheet import StudyDesignInterventionSheet
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
from usdm_excel.study_design_dictionary_sheet.study_design_dictionary_sheet import StudyDesignDictionarySheet
from usdm_excel.study_design_eligibility_criteria_sheet.study_design_eligibility_criteria_sheet import StudyDesignEligibilityCriteriaSheet
from usdm_excel.study_design_sites_sheet.study_design_sites_sheet import StudyDesignSitesSheet
from usdm_excel.study_design_conditions_sheet.study_design_conditions_sheet import StudyDesignConditionSheet
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
from usdm_model.study_title import StudyTitle
import traceback
import datetime

class StudySheet(BaseSheet):

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

      # Process all the sheets
      self._process_sheet()
      self.timings = StudyDesignTimingSheet(file_path)
      self.study_amendments = StudyDesignAmendmentSheet(file_path)
      self.study_identifiers = StudyIdentifiersSheet(file_path)
      self.procedures = StudyDesignProcedureSheet(file_path)
      self.encounters = StudyDesignEncounterSheet(file_path)
      self.elements = StudyDesignElementSheet(file_path)
      self.arms = StudyDesignArmSheet(file_path)
      self.epochs = StudyDesignEpochSheet(file_path)
      self.activities = StudyDesignActivitySheet(file_path)
      self.study_design = StudyDesignSheet(file_path)
      self._process_soa(file_path)
      self.indications = StudyDesignIndicationSheet(file_path)
      self.interventions = StudyDesignInterventionSheet(file_path)
      self.study_population = StudyDesignPopulationSheet(file_path)
      self.contents = StudyDesignContentSheet(file_path)
      self.dictionaries = StudyDesignDictionarySheet(file_path)
      self.oe = StudyDesignObjectiveEndpointSheet(file_path)
      self.eligibility_criteria = StudyDesignEligibilityCriteriaSheet(file_path)
      self.estimands = StudyDesignEstimandsSheet(file_path)
      self.sites = StudyDesignSitesSheet(file_path)
      self.conditions = StudyDesignConditionSheet(file_path)

      # Study Design assembly
      study_design = self.study_design.study_designs[0]
      study_design.scheduleTimelines.append(self.soa.timeline)
      study_design.encounters = self.encounters.items
      study_design.activities = self.soa.activities
      activity_ids = [item.id for item in study_design.activities]
      study_design.biomedicalConcepts = self.soa.biomedical_concepts
      study_design.bcSurrogates = self.soa.biomedical_concept_surrogates
      for key,tl in self.timelines.items():
        study_design.scheduleTimelines.append(tl.timeline)
        for activity in tl.activities:
          if activity.id not in activity_ids:
            study_design.activities.append(activity)
            activity_ids.append(activity.id)
        study_design.biomedicalConcepts += tl.biomedical_concepts
        study_design.bcSurrogates += tl.biomedical_concept_surrogates
      study_design.indications = self.indications.items
      study_design.studyInterventions = self.interventions.items
      study_design.population = self.study_population.population
      study_design.objectives = self.oe.objectives
      study_design.estimands = self.estimands.estimands
      study_design.population.criteria = self.eligibility_criteria.items
      study_design.dictionaries = self.dictionaries.items
      study_design.organizations = self.sites.organizations
      study_design.conditions = self.conditions.items

      # Final assembly
      try:
        self.protocol_document_version = StudyProtocolDocumentVersion(
          id=id_manager.build_id(StudyProtocolDocumentVersion), 
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
        self.study_version = StudyVersion(
          id=id_manager.build_id(StudyVersion),
          #studyTitle=self.title,
          versionIdentifier=self.version,
          type=self.type,
          studyPhase=self.phase,
          businessTherapeuticAreas=self.therapeutic_areas,
          rationale=self.rationale,
          #studyAcronym=self.acronym,
          studyIdentifiers=self.study_identifiers.identifiers,
          documentVersionId=self.protocol_document_version.id,
          studyDesigns=self.study_design.study_designs,
          dateValues=self.dates[self.STUDY_VERSION_DATE],
          amendments=self.study_amendments.items,
          titles=self.titles
        )
        cross_references.add(self.study_version.id, self.study_version)
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
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  # def study_sponsor(self):
  #   return self.cdisc_code(code="C93453", decode="Study Registry")

  # def study_regulatory(self):
  #   return self.cdisc_code(code="C93453", decode="Study Registry")

  def the_study(self):
    return self.study
  
  def api_root(self):
    return Wrapper(study=self.study)

  def to_html(self):
    return NarrativeContent(self.title, self.study).to_html()

  def to_pdf(self):
    return NarrativeContent(self.title, self.study).to_pdf()

  def _process_sheet(self):
    fields = ['category', 'name', 'description', 'label', 'type', 'date', 'scopes']    
    for rindex, row in self.sheet.iterrows():
      field_name = self.read_cell(rindex, self.PARAMS_NAME_COL)
      if field_name == self.NAME_TITLE:
        self.name = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.TITLE_TITLE:
        if option_manager.get(Options.USDM_VERSION) == '2':
          self.title = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.VERSION_TITLE:
        self.version = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.TYPE_TITLE:
        self.type = self.read_cdisc_klass_attribute_cell('Study', 'studyType', rindex, self.PARAMS_DATA_COL)
      elif field_name == self.PHASE_TITLE:
        phase = self.read_cdisc_klass_attribute_cell('Study', 'studyPhase', rindex, self.PARAMS_DATA_COL)
        self.phase = Alias().code(phase, [])
      elif field_name == self.ACRONYM_TITLE:
        self.acronym = self._set_title(rindex, self.PARAMS_DATA_COL, "Study Acronym")
        #self.acronym = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.RATIONALE_TITLE:
        self.rationale = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.TA_TITLE:
        self.therapeutic_areas = self.read_other_code_cell_mutiple(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.BRIEF_TITLE_TITLE:
        self.brief_title = self._set_title(rindex, self.PARAMS_DATA_COL, "Brief Study Title")
        #self.brief_title = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.OFFICAL_TITLE_TITLE:
        self.official_title = self._set_title(rindex, self.PARAMS_DATA_COL, "Official Study Title")
        #self.official_title = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.PUBLIC_TITLE_TITLE:
        self.public_title = self._set_title(rindex, self.PARAMS_DATA_COL, "Public Study Title")
        #self.public_title = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif field_name == self.SCIENTIFIC_TITLE_TITLE:
        self.scientific_title = self._set_title(rindex, self.PARAMS_DATA_COL, "Scientific Study Title")
        #self.scientific_title = self.read_cell(rindex, self.PARAMS_DATA_COL)
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
            dateValue=record['date'],
            geographicScopes=scopes
          )
          self.dates[category].append(date)
          cross_references.add(record['name'], date)
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

  def _set_title(self, rindex, cindex, title_type):
    if option_manager.get(Options.USDM_VERSION) == '2':
      return self.read_cell(rindex, cindex)
    else:
      try:
        code = CDISCCT().code_for_attribute('StudyVersion', 'titles', title_type)
        text = self.read_cell(rindex, cindex)
        title = StudyTitle(id=id_manager.build_id(StudyTitle), text=text, type=code)
        self.titles.append(title)
        cross_references.add(title.id, title)
        return title
      except Exception as e:
        self._error(rindex, cindex, "Failed to create StudyTitle object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")
        