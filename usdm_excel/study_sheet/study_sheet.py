from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_identifiers_sheet.study_identifiers_sheet import StudyIdentifiersSheet
from usdm_excel.study_design_sheet.study_design_sheet import StudyDesignSheet
from usdm_excel.study_soa_sheet.study_soa_sheet import StudySoASheet
from usdm_excel.indications_interventions.indication_interventions_sheet import IndicationsInterventionsSheet
from usdm_excel.study_design_population_sheet.study_design_population_sheet import StudyDesignPopulationSheet
from usdm_excel.study_design_objective_endpoint_sheet.study_design_objective_endpoint_sheet import StudyDesignObjectiveEndpointSheet
from usdm_excel.study_design_estimands_sheet.study_design_estimands_sheet import StudyDesignEstimandsSheet
from usdm_excel.alias import Alias
from usdm.study import Study
from usdm.study_protocol_version import StudyProtocolVersion
import traceback
import pandas as pd
import datetime

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

  def __init__(self, file_path, id_manager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='study', header=None), id_manager)
      self.phase = None
      self.version = None
      self.type = None
      self.title = None
      self.acronym = None
      self.rationale = None
      self.study = None
      self.protocols = []
      self.therapeutic_areas = []
      self._process_sheet()
      self.study_identifiers = StudyIdentifiersSheet(file_path, id_manager)
      self.study_design = StudyDesignSheet(file_path, id_manager)
      self.soa = StudySoASheet(file_path, id_manager)
      self.ii = IndicationsInterventionsSheet(file_path, id_manager)
      self.study_populations = StudyDesignPopulationSheet(file_path, id_manager)
      self.oe = StudyDesignObjectiveEndpointSheet(file_path, id_manager)
      self.estimands = StudyDesignEstimandsSheet(file_path, id_manager)

      for epoch in self.study_design.epochs:
        epoch.encounterIds = self.soa.epoch_encounter_map(epoch.studyEpochName)

      study_design = self.study_design.study_designs[0]
      study_design.studyScheduleTimelines.append(self.soa.timelines[0])
      study_design.encounters = self.soa.encounters
      study_design.activities = self.soa.activities
      study_design.biomedicalConcepts = self.soa.biomedical_concepts
      study_design.bcSurrogates = self.soa.biomedical_concept_surrogates
      study_design.studyIndications = self.ii.indications
      study_design.studyInvestigationalInterventions = self.ii.interventions
      study_design.studyStudyDesignPopulations = self.study_populations.populations
      study_design.studyObjectives = self.oe.objectives
      study_design.studyEstimands = self.estimands.estimands

      self.study = Study(
        studyId=None, # No Id, will be allocated a UUID
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
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()

  def study_sponsor(self):
    return self.cdisc_code(code="C93453", decode="Study Registry")

  def study_regulatory(self):
    return self.cdisc_code(code="C93453", decode="Study Registry")

  def the_study(self):
    return self.study
  
  def _process_sheet(self):
    fields = [ 'briefTitle', 'officialTitle', 'publicTitle', 'scientificTitle', 'protocolVersion', 'protocolAmendment', 'protocolEffectiveDate', 'protocolStatus' ]    
    for rindex, row in self.sheet.iterrows():
      if rindex == self.TITLE_ROW:
        self.title = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.VERSION_ROW:
        self.version = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.TYPE_ROW:
        self.type = self.cdisc_klass_attribute_cell('Study', 'studyType', self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
      elif rindex == self.PHASE_ROW:
        phase = self.cdisc_klass_attribute_cell('Study', 'studyPhase', self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
        self.phase = Alias(self.id_manager).code(phase, [])
      elif rindex == self.ACRONYM_ROW:
        self.acronym = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.RATIONALE_ROW:
        self.rationale = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.TA_ROW:
        self.therapeutic_areas = self.other_code_cell_mutiple(self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
        #print("8", self.therapeutic_areas)
      elif rindex >= self.PROTOCOL_DATA_ROW:
        record = {}
        for cindex in range(0, len(self.sheet.columns)):
          cell = self.clean_cell_unnamed(rindex, cindex)
          field = fields[cindex]
          if field == 'protocolStatus':
            record[field] = self.cdisc_klass_attribute_cell('StudyProtocolVersion', 'protocolStatus', cell) 
          elif field == 'protocolEffectiveDate':
            record[field] = datetime.datetime.strptime(cell, '%Y-%m-%d %H:%M:%S')
          else:
            record[field] = cell
        record['studyProtocolVersionId'] = self.id_manager.build_id(StudyProtocolVersion)
        spv = StudyProtocolVersion(**record)
        self.protocols.append(spv)
  