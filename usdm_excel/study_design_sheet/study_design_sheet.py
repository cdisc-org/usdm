from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm.study_epoch import StudyEpoch
from usdm.study_arm import StudyArm
from usdm.study_cell import StudyCell
from usdm.study_design import StudyDesign
from usdm_excel.alias import Alias
import pandas as pd
import traceback

class StudyDesignSheet(BaseSheet):

  TA_ROW = 0
  RATIONALE_ROW = 1
  BLINDING_ROW = 2
  INTENT_ROW = 3
  TYPES_ROW = 4
  INT_ROW = 5
  MAIN_TIMELINE_ROW = 6
  OTHER_TIMELINES_ROW = 7

  EPOCH_ARMS_START_ROW = 9
  
  PARAMS_DATA_COL = 1

  def __init__(self, file_path):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesign', header=None))
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
      print("Oops! (Design Sheet)", e, "occurred.")
      traceback.print_exc()

  def process_sheet(self):
    for rindex, row in self.sheet.iterrows():
      if rindex == self.TA_ROW:
        self.therapeutic_areas = self.other_code_cell_mutiple(self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
      elif rindex == self.RATIONALE_ROW:
        self.rationale = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.BLINDING_ROW:
        self.blinding = Alias().code(self.cdisc_klass_attribute_cell('StudyDesign', 'studyDesignBlindingScheme', self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)), [])
      elif rindex == self.INTENT_ROW:
        self.trial_intents = self.cdisc_klass_attribute_cell_multiple('StudyDesign', 'trialIntentType', self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
      elif rindex == self.TYPES_ROW:
        self.trial_types = self.cdisc_klass_attribute_cell_multiple('StudyDesign', 'trialType', self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
      elif rindex == self.INT_ROW:
        self.intervention_model = self.cdisc_klass_attribute_cell('StudyDesign', 'interventionModel', self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
      elif rindex == self.MAIN_TIMELINE_ROW:
        self.main_timeline = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.OTHER_TIMELINES_ROW:
        self.other_timelines = self.clean_cell_unnamed_multiple(rindex, self.PARAMS_DATA_COL)
      else:
        pass

    for rindex, row in self.sheet.iterrows():
      if rindex >= self.EPOCH_ARMS_START_ROW:
        for cindex in range(0, len(self.sheet.columns)):
          cell = self.clean_cell_unnamed(rindex, cindex)
          if rindex == self.EPOCH_ARMS_START_ROW:
            if cindex != 0:
              epoch = self._add_epoch(cell, cell)
              self.epochs.append(epoch)
          else:
            if cindex == 0:
              self.arms.append(self._add_arm(cell, cell))
            else:
              elements = []
              element_names = self.clean_cell_unnamed_multiple(rindex, cindex)
              print("ELEMENTS:", element_names)
              for name in element_names:
                elements.append(cross_references.get(name))
              self.cells.append(self._add_cell(arm=self.arms[-1], epoch=self.epochs[cindex-1], elements=elements))
    
    self.double_link(self.epochs, 'studyEpochId', 'previousStudyEpochId', 'nextStudyEpochId')

    study_design = self._add_design(
      name="Excel Study",
      description="",
      cells=self.cells, 
      intent_types=self.trial_intents, 
      trial_types=self.trial_types, 
      intervention_model=self.intervention_model,
      rationale=self.rationale, 
      blinding=self.blinding, 
      therapeutic_areas=self.therapeutic_areas
    )
    self.study_designs.append(study_design)

  def _add_arm(self, name, description):
    arm_origin = self.cdisc_code_cell("C188866=Data Generated Within Study")
    return StudyArm(
      studyArmId=id_manager.build_id(StudyArm), 
      studyArmName=name,
      studyArmDescription=description,
      studyArmType="",
      studyArmDataOriginDescription="",
      studyArmDataOriginType=arm_origin
    )

  def _add_epoch(self, name, description):
    epoch_type = self.cdisc_code_cell("C165873=OBSERVATION")
    return StudyEpoch(
      studyEpochId=id_manager.build_id(StudyEpoch), 
      studyEpochName=name, 
      studyEpochDescription=description,
      studyEpochType=epoch_type
    )
  
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
