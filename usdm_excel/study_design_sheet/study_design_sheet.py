from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import IdManager
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

  EPOCH_ARMS_START_ROW = 7
  
  PARAMS_DATA_COL = 1

  def __init__(self, file_path, id_manager: IdManager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesign', header=None), id_manager)
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
      self.process_sheet()
    except Exception as e:
      print("Oops! (Design Sheet)", e, "occurred.")
      traceback.print_exc()

  def process_sheet(self):
    for rindex, row in self.sheet.iterrows():
      if rindex == self.TA_ROW:
        items = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
        parts = items.split(",")
        for part in parts:
          pass
          #print("TA", items, part)
      elif rindex == self.RATIONALE_ROW:
        self.rationale = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.BLINDING_ROW:
        self.blinding = Alias(self.id_manager).code(self.cdisc_code_cell(self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)), [])
      elif rindex == self.INTENT_ROW:
        self.trial_intents = self.cdisc_code_set_cell(self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
      elif rindex == self.TYPES_ROW:
        self.trial_types = self.cdisc_code_set_cell(self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
      elif rindex == self.INT_ROW:
        self.intervention_model = self.cdisc_code_cell(self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
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
              self.cells.append(self._add_cell(arm=self.arms[-1], epoch=self.epochs[cindex-1]))

    
    
    #self.double_link(self.epochs, 'studyEpochId', 'previousStudyEpochId', 'nextStudyEpochId')
    
              
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

  # def link_encounters(self, encounter_map):
  #   for epoch_name, encounters in encounter_map.items():
  #     #print("LINK: %s %s" % (epoch_name, encounter))
  #     epoch = self.epoch_map[epoch_name]
  #     for encounter in encounters:
  #       epoch.encounters.append(encounter)
  
  # def link_timelines(self, timelines):
  #   self.study_designs[0]['studyScheduleTimelines'].append(timelines)

  def _add_arm(self, name, description):
    arm_origin = self.cdisc_code_cell("C188866=Data Generated Within Study")
    return StudyArm(
      studyArmId=self.id_manager.build_id(StudyArm), 
      studyArmName=name,
      studyArmDescription=description,
      studyArmType="",
      studyArmDataOriginDescription="",
      studyArmDataOriginType=arm_origin
    )

  def _add_epoch(self, name, description):
    epoch_type = self.cdisc_code_cell("C165873=OBSERVATION")
    return StudyEpoch(
      studyEpochId=self.id_manager.build_id(StudyEpoch), 
      studyEpochName=name, 
      studyEpochDescription=description,
      studyEpochType=epoch_type
    )
  
  def _add_cell(self, arm, epoch):
    return StudyCell(
      studyCellId=self.id_manager.build_id(StudyCell), 
      studyArm=arm,
      studyEpoch=epoch
    )

  def _add_design(self, name, description, cells, intent_types, trial_types, intervention_model, rationale, blinding, therapeutic_areas):
    return StudyDesign(
      studyDesignId=self.id_manager.build_id(StudyDesign), 
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
