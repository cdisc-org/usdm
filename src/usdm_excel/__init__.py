import traceback

from usdm_excel.configuration_sheet import ConfigurationSheet
from usdm_excel.study_sheet.study_sheet import StudySheet
from usdm_excel.errors.errors import Errors
from usdm_excel.managers import Managers
from usdm_model.wrapper import Wrapper
from usdm_info import __model_version__ as usdm_version, __package_version__ as system_version

from usdm_excel.study_identifiers_sheet.study_identifiers_sheet import StudyIdentifiersSheet
from usdm_excel.study_design_sheet.study_design_sheet import StudyDesignSheet
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

from usdm_model.study import Study
from usdm_model.study_version import StudyVersion
from usdm_model.study_protocol_document_version import StudyProtocolDocumentVersion
from usdm_model.study_protocol_document import StudyProtocolDocument
from usdm_model.wrapper import Wrapper

class USDMExcel():

  SYSTEM_NAME = "CDISC USDM E2J"

  def __init__(self, file_path):
    self._managers = Managers()
    self._file_path = file_path

  def execute(self):
    self._process()

  def errors(self):
    return self._managers.errors.dump(Errors.WARNING)
  
  def _process(self, file_path):
    try:
    
      # Process all the sheets
      self.study = StudySheet(self._file_path, self._managers)
      self.timings = StudyDesignTimingSheet(self._file_path, self.manager)
      self.study_amendments = StudyDesignAmendmentSheet(self._file_path, self.manager)
      self.study_identifiers = StudyIdentifiersSheet(self._file_path, self.manager)
      self.procedures = StudyDesignProcedureSheet(self._file_path, self.manager)
      self.encounters = StudyDesignEncounterSheet(self._file_path, self.manager)
      self.elements = StudyDesignElementSheet(self._file_path, self.manager)
      self.arms = StudyDesignArmSheet(self._file_path, self.manager)
      self.epochs = StudyDesignEpochSheet(self._file_path, self.manager)
      self.activities = StudyDesignActivitySheet(self._file_path, self.manager)
      self.study_design = StudyDesignSheet(self._file_path, self.manager)
      self._process_soa(file_path)
      self.indications = StudyDesignIndicationSheet(self._file_path, self.manager)
      self.interventions = StudyDesignInterventionSheet(self._file_path, self.manager)
      self.study_population = StudyDesignPopulationSheet(self._file_path, self.manager)
      self.contents = StudyDesignContentSheet(self._file_path, self.manager)
      self.dictionaries = StudyDesignDictionarySheet(self._file_path, self.manager)
      self.oe = StudyDesignObjectiveEndpointSheet(self._file_path, self.manager)
      self.eligibility_criteria = StudyDesignEligibilityCriteriaSheet(self._file_path, self.manager)
      self.estimands = StudyDesignEstimandsSheet(self._file_path, self.manager)
      self.sites = StudyDesignSitesSheet(self._file_path, self.manager)
      self.conditions = StudyDesignConditionSheet(self._file_path, self.manager)

      # Study Design assembly
      study_design = self.study_design.study_designs[0]
      study_design.scheduleTimelines.append(self.soa.timeline)
      study_design.encounters = self.encounters.items
      study_design.activities = self.soa.activities
      activity_ids = [item.id for item in study_design.activities]
      study_design.biomedicalConcepts = self.soa.biomedical_concepts
      study_design.bcSurrogates = self.soa.biomedical_concept_surrogates
      for key, tl in self.timelines.items():
        study_design.scheduleTimelines.append(tl.timeline)
        for activity in tl.activities:
          if activity.id not in activity_ids:
            study_design.activities.append(activity)
            activity_ids.append(activity.id)
        study_design.biomedicalConcepts += tl.biomedical_concepts
        study_design.bcSurrogates += tl.biomedical_concept_surrogates
      self.double_link(study_design.activities, 'previousId', 'nextId')
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
          id=self._managers.id_manager.build_id(StudyProtocolDocumentVersion), 
          protocolVersion=self.protocol_version,
          protocolStatus=self.protocol_status,
          dateValues=self.dates[self.PROTOCOL_VERSION_DATE]
          )
        self.protocol_document_version.contents = self.contents.items
        self._managers.cross_references.add(self.protocol_document_version.id, self.protocol_document_version)
      except Exception as e:
        self._general_error(f"Failed to create StudyProtocolDocumentVersion object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")

      try:
        study_protocol_document = StudyProtocolDocument(
          id=self._managers.id_manager.build_id(StudyProtocolDocument), 
          name=f"Protocol_Document_{self.name}", 
          versions=[self.protocol_document_version])
      except Exception as e:
        self._general_error(f"Failed to create StudyProtocolDocument object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")

      try:
        self.study_version = StudyVersion(
          id=self._managers.id_manager.build_id(StudyVersion),
          versionIdentifier=self.version,
          studyType=self.type,
          studyPhase=self.phase,
          businessTherapeuticAreas=self.therapeutic_areas,
          rationale=self.rationale,
          studyIdentifiers=self.study_identifiers.identifiers,
          documentVersionId=self.protocol_document_version.id,
          studyDesigns=self.study_design.study_designs,
          dateValues=self.dates[self.STUDY_VERSION_DATE],
          amendments=self.study_amendments.items,
          titles=self.titles
        )
        self._managers.cross_references.add(self.study_version.id, self.study_version)
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
        self._managers.cross_references.add("STUDY", self.study)
        self.contents.resolve(self.study) # Now we have full study, resolve references in the content
      except Exception as e:
        self._general_error(f"Failed to create Study object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")

      self.wrapper = Wrapper(study=self.study, usdmVersion=usdm_version, systemName=self.SYSTEM_NAME, systemVersion=system_version)
 
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def _process_soa(self, file_path):
    tls = []
    for timeline in self.study_design.other_timelines:
      tl = StudySoAV2Sheet(self._file_path, timeline, False)
      tls.append(tl)
      self.timelines[timeline] = tl
      self._managers.cross_references.add(timeline, tl.timeline)
    self.soa = StudySoAV2Sheet(self._file_path, self.study_design.main_timeline, True)
    tls.append(self.soa)
    self._set_timing_references(tls)
    self._check_timing_references(tls)

  def _check_timing_references(self, tls):
    timing_check = {}
    for timing in self.timings.items:
      timing_check[timing.name] = None
    for tl in tls:
      tl_items = tl.check_timing_references(self.timings.items, timing_check)
      tl.timeline.timings = tl_items
    for timing in self.timings.items:
      if not timing_check[timing.name]:
        self._general_warning(f"Timing with name '{timing.name}' not referenced")

  def _set_timing_references(self, tls):
    for timing in self.timings.items:
      found = {'from': False, 'to': False}
      for tl in tls:
        if not found['from']:
          instance = tl.timing_match(timing.relativeFromScheduledInstanceId)
          if instance:
            item = instance.item
            timing.relativeFromScheduledInstanceId = item.id
            found['from'] = True
        if not found['to']:
          instance = tl.timing_match(timing.relativeToScheduledInstanceId)
          if instance:
            item = instance.item
            timing.relativeToScheduledInstanceId = item.id
            found['to'] = True
      if not found['from']:
        self._general_error(f"Unable to find timing 'from' reference with name {timing.relativeFromScheduledInstanceId}")
      if not found['to']:
        self._general_error(f"Unable to find timing 'to' reference with name {timing.relativeToScheduledInstanceId}")
