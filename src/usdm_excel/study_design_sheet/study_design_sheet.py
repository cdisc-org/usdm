from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_model.study_epoch import StudyEpoch
from usdm_model.study_arm import StudyArm
from usdm_model.study_cell import StudyCell
from usdm_model.study_design import StudyDesign
from usdm_excel.alias import Alias
import pandas as pd
import traceback

class StudyDesignSheet(BaseSheet):

  NAME_ROW = 0
  DESCRIPTION_ROW = 1
  TA_ROW = 2
  RATIONALE_ROW = 3
  BLINDING_ROW = 4
  INTENT_ROW = 5
  TYPES_ROW = 6
  INT_ROW = 7
  MAIN_TIMELINE_ROW = 8
  OTHER_TIMELINES_ROW = 9

  EPOCH_ARMS_START_ROW = 11
  
  PARAMS_DATA_COL = 1

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesign', header=None)
      self.name = "TEST"
      self.description = "An Microsoft Excel test study design"
      self.epochs = []
      self.arms = []
      self.cells = []
      self.study_designs = []
      self.therapeutic_areas = []
      self.rationale = ""
      self.blinding = None
      self.trial_intents = []
      self.trial_types = []
      self.intervention_model = None
      self.main_timeline = None
      self.other_timelines = []
      self.process_sheet()
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def process_sheet(self):
    for rindex, row in self.sheet.iterrows():
      if rindex == self.NAME_ROW:
        self.name = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.DESCRIPTION_ROW:
        self.description = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.TA_ROW:
        self.therapeutic_areas = self.read_other_code_cell_mutiple(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.RATIONALE_ROW:
        self.rationale = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.BLINDING_ROW:
        self.blinding = Alias().code(self.read_cdisc_klass_attribute_cell('StudyDesign', 'studyDesignBlindingScheme',rindex, self.PARAMS_DATA_COL), [])
      elif rindex == self.INTENT_ROW:
        self.trial_intents = self.read_cdisc_klass_attribute_cell_multiple('StudyDesign', 'trialIntentType', rindex, self.PARAMS_DATA_COL)
      elif rindex == self.TYPES_ROW:
        self.trial_types = self.read_cdisc_klass_attribute_cell_multiple('StudyDesign', 'trialType', rindex, self.PARAMS_DATA_COL)
      elif rindex == self.INT_ROW:
        self.intervention_model = self.read_cdisc_klass_attribute_cell('StudyDesign', 'interventionModel', rindex, self.PARAMS_DATA_COL)
      elif rindex == self.MAIN_TIMELINE_ROW:
        self.main_timeline = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.OTHER_TIMELINES_ROW:
        self.other_timelines = self.read_cell_multiple(rindex, self.PARAMS_DATA_COL)
      else:
        pass

    for rindex, row in self.sheet.iterrows():
      if rindex >= self.EPOCH_ARMS_START_ROW:
        for cindex in range(0, len(self.sheet.columns)):
          cell = self.read_cell(rindex, cindex)
          if rindex == self.EPOCH_ARMS_START_ROW:
            if cindex != 0:
              epoch = self._add_epoch(cell)
              self.epochs.append(epoch)
          else:
            if cindex == 0:
              self.arms.append(self._add_arm(cell))
            else:
              elements = []
              element_names = self.read_cell_multiple(rindex, cindex)
              for name in element_names:
                elements.append(cross_references.get(name))
              self.cells.append(self._add_cell(arm=self.arms[-1], epoch=self.epochs[cindex-1], elements=elements))
    
    self.double_link(self.epochs, 'studyEpochId', 'previousStudyEpochId', 'nextStudyEpochId')

    study_design = self._add_design(
      name=self.name,
      description=self.description,
      cells=self.cells, 
      intent_types=self.trial_intents, 
      trial_types=self.trial_types, 
      intervention_model=self.intervention_model,
      rationale=self.rationale, 
      blinding=self.blinding, 
      therapeutic_areas=self.therapeutic_areas
    )
    self.study_designs.append(study_design)

  def _add_arm(self, name):
    return cross_references.get(name)

  def _add_epoch(self, name):
    return cross_references.get(name)
  
  def _add_cell(self, arm, epoch, elements):
    return StudyCell(
      studyCellId=id_manager.build_id(StudyCell), 
      studyArm=arm,
      studyEpoch=epoch,
      studyElements=elements
    )

  def _add_design(self, name, description, cells, intent_types, trial_types, intervention_model, rationale, blinding, therapeutic_areas):
    return StudyDesign(
      studyDesignId=id_manager.build_id(StudyDesign), 
      studyDesignName=name,
      studyDesignDescription=description,
      trialIntentTypes=intent_types,
      trialType=trial_types,
      interventionModel=intervention_model,
      studyCells=cells,
      therapeuticAreas=therapeutic_areas,
      studyDesignRationale=rationale,
      studyDesignBlindingScheme=blinding
    )
