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
import traceback
import pandas as pd
from usdm_excel.cdisc_ct import CDISCCT

class StudySheet(BaseSheet):

  def __init__(self, file_path, id_manager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='study'), id_manager)
      self.study = None
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

      for index, row in self.sheet.iterrows():
        study_phase = Alias(self.id_manager).code(self.cdisc_klass_attribute_cell('Study', 'studyPhase', self.clean_cell(row, index, "studyPhase")), [])
        study_version = self.clean_cell(row, index, "studyVersion")
        study_type = self.cdisc_klass_attribute_cell('Study', 'studyType', self.clean_cell(row, index, "studyType"))
        study_title = self.clean_cell(row, index, "studyTitle")
        self.study = Study(
          studyId=None, # No Id, will be allocated a UUID
          studyTitle=study_title,
          studyVersion=study_version,
          studyType=study_type,
          studyPhase=study_phase,
          businessTherapeuticAreas=[],
          studyRationale="",
          studyAcronym="",
          studyIdentifiers=self.study_identifiers.identifiers,
          studyProtocolVersions=[],
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