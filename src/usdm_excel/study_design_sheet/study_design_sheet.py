from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_model.study_epoch import StudyEpoch
from usdm_model.study_arm import StudyArm
from usdm_model.study_element import StudyElement
from usdm_model.study_cell import StudyCell
from usdm_model.study_design import StudyDesign
from usdm_excel.alias import Alias
import pandas as pd
import traceback

class StudyDesignSheet(BaseSheet):

  VERSION_ROWS = { 
    'therapeuticAreas': {
      'NAME_ROW': 0,
      'DESCRIPTION_ROW': 1,
      'LABEL_ROW': -1,
      'TA_ROW': 2,
      'RATIONALE_ROW': 3,
      'BLINDING_ROW': 4,
      'INTENT_ROW': 5,
      'TYPES_ROW': 6,
      'INT_ROW': 7,
      'MAIN_TIMELINE_ROW': 8,
      'OTHER_TIMELINES_ROW': 9,
      'EPOCH_ARMS_START_ROW': 11
    },
    'label': { 
      'NAME_ROW': 0,
      'DESCRIPTION_ROW': 1,
      'LABEL_ROW': 2,
      'TA_ROW': 3,
      'RATIONALE_ROW': 4,
      'BLINDING_ROW': 5,
      'INTENT_ROW': 6,
      'TYPES_ROW': 7,
      'INT_ROW': 8,
      'MAIN_TIMELINE_ROW': 9,
      'OTHER_TIMELINES_ROW': 10,
      'EPOCH_ARMS_START_ROW': 12
    }
  }

  CHECK_ROW = 2
  PARAMS_NAME_COL = 0
  PARAMS_DATA_COL = 1

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesign', header=None)
      self.name = "TEST"
      self.description = "An Microsoft Excel test study design"
      self.label=""
      self.epochs = []
      self.epoch_names = {}
      self.arms = []
      self.arm_names = {}
      self.cells = []
      self.elements = {}
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
    key = self.read_cell(self.CHECK_ROW, self.PARAMS_NAME_COL)
    for rindex, row in self.sheet.iterrows():
      if rindex == self.VERSION_ROWS[key]['NAME_ROW']:
        self.name = self.read_cell(rindex, self.PARAMS_DATA_COL)
      if rindex == self.VERSION_ROWS[key]['LABEL_ROW']:
        self.label = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.VERSION_ROWS[key]['DESCRIPTION_ROW']:
        self.description = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.VERSION_ROWS[key]['TA_ROW']:
        self.therapeutic_areas = self.read_other_code_cell_mutiple(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.VERSION_ROWS[key]['RATIONALE_ROW']:
        self.rationale = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.VERSION_ROWS[key]['BLINDING_ROW']:
        self.blinding = Alias().code(self.read_cdisc_klass_attribute_cell('StudyDesign', 'studyDesignBlindingScheme',rindex, self.PARAMS_DATA_COL), [])
      elif rindex == self.VERSION_ROWS[key]['INTENT_ROW']:
        self.trial_intents = self.read_cdisc_klass_attribute_cell_multiple('StudyDesign', 'trialIntentType', rindex, self.PARAMS_DATA_COL)
      elif rindex == self.VERSION_ROWS[key]['TYPES_ROW']:
        self.trial_types = self.read_cdisc_klass_attribute_cell_multiple('StudyDesign', 'trialType', rindex, self.PARAMS_DATA_COL)
      elif rindex == self.VERSION_ROWS[key]['INT_ROW']:
        self.intervention_model = self.read_cdisc_klass_attribute_cell('StudyDesign', 'interventionModel', rindex, self.PARAMS_DATA_COL)
      elif rindex == self.VERSION_ROWS[key]['MAIN_TIMELINE_ROW']:
        self.main_timeline = self.read_cell(rindex, self.PARAMS_DATA_COL)
      elif rindex == self.VERSION_ROWS[key]['OTHER_TIMELINES_ROW']:
        self.other_timelines = self.read_cell_multiple(rindex, self.PARAMS_DATA_COL)
      else:
        pass

    start_row = self.VERSION_ROWS[key]['EPOCH_ARMS_START_ROW']
    resolved_epochs = [None] * self.sheet.shape[1] 
    resolved_arms = [None] * self.sheet.shape[0] 
    for rindex, row in self.sheet.iterrows():
      if rindex >= start_row:
        for cindex in range(0, len(self.sheet.columns)):
          epoch_index = cindex - 1
          cell = self.read_cell(rindex, cindex)
          if rindex == start_row:
            if cindex != 0:
              resolved_epochs[epoch_index] = self._add_epoch(cell)
          else:
            arm_index = rindex - start_row - 1
            if cindex == 0:
              resolved_arms[arm_index] = self._add_arm(cell)
            else:
              cell_elements = []
              element_names = self.read_cell_multiple(rindex, cindex)
              for name in element_names:
                element = self._add_element(name)
                if element is not None:
                  cell_elements.append(element.id)
              cell_arm = resolved_arms[arm_index].id
              cell_epoch = resolved_epochs[epoch_index].id
              if cell_arm is not None and cell_epoch is not None:
                self.cells.append(self._add_cell(arm=cell_arm, epoch=cell_epoch, elements=cell_elements))
              else:
                self._general_error(f"Cannot resolve arm and/or epoch for cell [{arm_index + 1},{epoch_index + 1}]")
              
    self.double_link(self.epochs, 'previousStudyEpochId', 'nextStudyEpochId')

    study_design = self._add_design(
      name=self.name,
      description=self.description,
      label=self.label,
      cells=self.cells,
      epochs=self.epochs,
      arms=self.arms,
      elements=list(self.elements.values()),
      intent_types=self.trial_intents, 
      trial_types=self.trial_types, 
      intervention_model=self.intervention_model,
      rationale=self.rationale, 
      blinding=self.blinding, 
      therapeutic_areas=self.therapeutic_areas
    )
    self.study_designs.append(study_design)

  def _add_arm(self, name):
    arm = cross_references.get(StudyArm, name)
    if arm is not None:
      if name not in self.arm_names:
        self.arm_names[name] = True
        self.arms.append(arm)
      return arm
    else:
      self._general_error(f"No arm definition found for arm '{name}'")
      return None

  def _add_epoch(self, name):
    epoch = cross_references.get(StudyEpoch, name)
    if epoch is not None:
      if name not in self.epoch_names:
        self.epoch_names[name] = True
        self.epochs.append(epoch)
      return epoch
    else:
      self._general_error(f"No epoch definition found for epoch '{name}'")
      return None
  
  def _add_element(self, name):
    element = cross_references.get(StudyElement, name)
    if element is not None:
      if name not in self.elements:
        self.elements[name] = element
      return element
    else:
      self._general_error(f"No element definition found for element '{name}'")
      return None

  def _add_cell(self, arm, epoch, elements):
    return StudyCell(
      id=id_manager.build_id(StudyCell), 
      studyArmId=arm,
      studyEpochId=epoch,
      studyElementIds=elements
    )

  def _add_design(self, name, description, label, epochs, arms, cells, elements, intent_types, trial_types, intervention_model, rationale, blinding, therapeutic_areas):
    return StudyDesign(
      id=id_manager.build_id(StudyDesign), 
      name=name,
      description=description,
      label=label,
      trialIntentTypes=intent_types,
      trialTypes=trial_types,
      interventionModel=intervention_model,
      studyCells=cells,
      studyArms=arms,
      studyEpochs=epochs,
      studyElements=elements,
      therapeuticAreas=therapeutic_areas,
      studyDesignRationale=rationale,
      studyDesignBlindingScheme=blinding,
      contents=[]
    )
