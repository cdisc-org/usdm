from pydantic import BaseModel
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_identifiers_sheet.study_identifiers_sheet import StudyIdentifiersSheet
from usdm_excel.study_design_sheet.study_design_sheet import StudyDesignSheet
from usdm_excel.study_soa_sheet.study_soa_sheet import StudySoASheet
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
from usdm_excel.alias import Alias
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.option_manager import *
from usdm_model.api_base_model import ApiBaseModel
from usdm_model.study import Study
from usdm_model.study_protocol_version import StudyProtocolVersion
import traceback
import pandas as pd
import datetime

class SDRRoot(ApiBaseModel):
  clinicalStudy: Study

class StudySheet(BaseSheet):

  TITLE_ROW = 0
  VERSION_ROW = 1
  TYPE_ROW = 2
  PHASE_ROW = 3
  ACRONYM_ROW = 4
  RATIONALE_ROW = 5
  TA_ROW = 6

  PROTOCOL_HEADER_ROW = 8
  PROTOCOL_DATA_ROW = 9
  
  PARAMS_DATA_COL = 1

  def __init__(self, file_path):
    try:
      #super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='study', header=None))
      super().__init__(file_path=file_path, sheet_name='study', header=None)
      self.phase = None
      self.version = None
      self.type = None
      self.title = None
      self.acronym = None
      self.rationale = None
      self.study = None
      self.protocols = []
      self.therapeutic_areas = []
      self.timelines = {}
      self._process_sheet()
      self.study_identifiers = StudyIdentifiersSheet(file_path)
      self.procedures = StudyDesignProcedureSheet(file_path)
      self.encounters = StudyDesignEncounterSheet(file_path)
      self.elements = StudyDesignElementSheet(file_path)
      self.arms = StudyDesignArmSheet(file_path)
      self.epochs = StudyDesignEpochSheet(file_path)
      self.activities = StudyDesignActivitySheet(file_path)
      self.study_design = StudyDesignSheet(file_path)
      for timeline in self.study_design.other_timelines:
        tl = StudySoASheet(file_path, timeline)
        self.timelines[timeline] = tl
        cross_references.add(timeline, tl.timeline.id)
      self.soa = StudySoASheet(file_path, self.study_design.main_timeline, True)
      self.ii = StudyDesignIISheet(file_path)
      self.study_populations = StudyDesignPopulationSheet(file_path)
      self.oe = StudyDesignObjectiveEndpointSheet(file_path)
      self.estimands = StudyDesignEstimandsSheet(file_path)

      # for epoch in self.study_design.epochs:
      #   ids = self.soa.epoch_encounter_map(epoch.studyEpochName)
      #   if ids is not None:
      #     epoch.encounterIds = ids
      #   else:
      #     self._general_info(f"No encounters found for epoch '{epoch.studyEpochName}'")

      study_design = self.study_design.study_designs[0]
      study_design.studyScheduleTimelines.append(self.soa.timeline)
      study_design.encounters = self.encounters.items
      study_design.activities = self.soa.activities
      study_design.biomedicalConcepts = self.soa.biomedical_concepts
      study_design.bcSurrogates = self.soa.biomedical_concept_surrogates
      for key,tl in self.timelines.items():
        study_design.studyScheduleTimelines.append(tl.timeline)
        study_design.activities += tl.activities
        study_design.biomedicalConcepts += tl.biomedical_concepts
        study_design.bcSurrogates += tl.biomedical_concept_surrogates
      study_design.studyIndications = self.ii.indications
      study_design.studyInvestigationalInterventions = self.ii.interventions
      study_design.studyPopulations = self.study_populations.populations
      study_design.studyObjectives = self.oe.objectives
      study_design.studyEstimands = self.estimands.estimands

      try:
        self.study = Study(
          id=None, # No Id, will be allocated a UUID
          studyTitle=self.title,
          studyVersion=self.version,
          studyType=self.type,
          studyPhase=self.phase,
          businessTherapeuticAreas=self.therapeutic_areas,
          studyRationale=self.rationale,
          studyAcronym=self.acronym,
          studyIdentifiers=self.study_identifiers.identifiers,
          studyProtocolVersions=self.protocols,
          studyDesigns=self.study_design.study_designs
        )
      except:
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
    if option_manager.get(Options.ROOT) == RootOption.SDR_COMPATABLE.value:
      root = SDRRoot(clinicalStudy=self.study)
    else:
      root = self.study
    return root

  def _process_sheet(self):
    fields = [ 'briefTitle', 'officialTitle', 'publicTitle', 'scientificTitle', 'protocolVersion', 'protocolAmendment', 'protocolEffectiveDate', 'protocolStatus' ]    
    for rindex, row in self.sheet.iterrows():
      if rindex == self.TITLE_ROW:
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
      elif rindex >= self.PROTOCOL_DATA_ROW:
        record = {}
        for cindex in range(0, len(self.sheet.columns)):
          field = fields[cindex]
          if field == 'protocolStatus':
            record[field] = self.read_cdisc_klass_attribute_cell('StudyProtocolVersion', 'protocolStatus', rindex, cindex) 
          elif field == 'protocolEffectiveDate':
            cell = self.read_cell(rindex, cindex)
            record[field] = datetime.datetime.strptime(cell, '%Y-%m-%d %H:%M:%S')
          else:
            cell = self.read_cell(rindex, cindex)
            record[field] = cell
        record['id'] = id_manager.build_id(StudyProtocolVersion)
        spv = StudyProtocolVersion(**record)
        self.protocols.append(spv)
  