from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import IdManager
from model.study_epoch import StudyEpoch
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
      self.epoch_map = {}
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
    #print("COLS", len(self.sheet.columns))
    for rindex, row in self.sheet.iterrows():
      if rindex == self.TA_ROW:
        items = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
        parts = items.split(",")
        for part in parts:
          print("TA", items, part)
      elif rindex == self.RATIONALE_ROW:
        self.rationale = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.BLINDING_ROW:
        self.blinding = self.cdisc_code_cell(self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
      elif rindex == self.INTENT_ROW:
        items = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
        parts = items.split(",")
        for part in parts:
          print("INTENT", items, part)
          self.trial_intents.append(self.cdisc_code_cell(part))
      elif rindex == self.TYPES_ROW:
        items = self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL)
        parts = items.split(",")
        for part in parts:
          print("TTYPE", items, part)
          self.trial_types.append(self.cdisc_code_cell(part))
      elif rindex == self.INT_ROW:
        self.intervention_model = self.cdisc_code_cell(self.clean_cell_unnamed(rindex, self.PARAMS_DATA_COL))
      else:
        pass

    for rindex, row in self.sheet.iterrows():
      if rindex >= self.EPOCH_ARMS_START_ROW:
        for cindex in range(0, len(self.sheet.columns)):
          cell = self.clean_cell_unnamed(rindex, cindex)
          #print("CELL [%s,%s] %s" % (rindex, cindex, cell))
          if rindex == self.EPOCH_ARMS_START_ROW:
            if cindex != 0:
              epoch = StudyEpoch(name=cell, description=cell)
              self.epoch_map[cell] = epoch
              self.epochs.append(epoch)
          else:
            if cindex == 0:
              self.arms.append(self.json_engine.add_study_arm(name=cell, description=cell))
            else:
              self.cells.append(self.json_engine.add_study_cell(arm=self.arms[-1], epoch=self.epochs[cindex-1]))

    self.double_link(self.epochs, 'studyEpochId', 'previousStudyEpochId', 'nextStudyEpochId')
    study_design = self.json_engine.add_study_design(
      cells=self.cells, 
      intent_types=self.trial_intents, 
      trial_types=self.trial_types, 
      intervention_model=self.intervention_model,
      rationale=self.rationale, 
      blinding=self.blinding, 
      therapeutic_areas=self.therapeutic_areas
    )
    print("STUDY_DESIGN:", study_design)
    self.study_designs.append(study_design)

  def link_encounters(self, encounter_map):
    for epoch_name, encounters in encounter_map.items():
      #print("LINK: %s %s" % (epoch_name, encounter))
      epoch = self.epoch_map[epoch_name]
      for encounter in encounters:
        epoch.encounters.append(encounter)
  
  def link_timelines(self, timelines):
    self.study_designs[0]['studyScheduleTimelines'].append(timelines)
