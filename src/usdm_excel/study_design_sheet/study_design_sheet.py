import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.study_epoch import StudyEpoch
from usdm_model.study_arm import StudyArm
from usdm_model.study_element import StudyElement
from usdm_model.study_cell import StudyCell
from usdm_model.study_design import StudyDesign
from usdm_model.masking import Masking
from usdm_excel.alias import Alias
from usdm_excel.option_manager import *
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.managers import Managers
from usdm_excel.utility import general_sheet_exception

class StudyDesignSheet(BaseSheet):

  SHEET_NAME = 'studyDesign'
  
  NAME_LABEL = ['studyDesignName', 'name']
  DESCRIPTION_LABEL = ['studyDesignDescription', 'description']
  LABEL_LABEL = ['label']
  TA_LABEL = ['therapeuticAreas']
  RATIONALE_LABEL = ['studyDesignRationale']
  BLINDING_LABEL = ['studyDesignBlindingScheme']
  INTENT_LABEL = ['trialIntentTypes']
  TYPES_LABEL = ['trialTypes']
  INT_LABEL = ['interventionModel']
  MAIN_TIMELINE_LABEL = ['mainTimeline']
  OTHER_TIMELINES_LABEL = ['otherTimelines']
  MASKING_ROLE_LABEL = ['masking']
  CHARACTERISTICS_LABEL = ['characteristics']

  PARAMS_NAME_COL = 0
  PARAMS_DATA_COL = 1

  def __init__(self, file_path: str, managers: Managers):
    try:
      super().__init__(file_path=file_path, managers=managers, sheet_name=self.SHEET_NAME, header=None)
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
      self.characteristics = []
      self.trial_types = []
      self.intervention_model = None
      self.main_timeline = None
      self.other_timelines = []
      self.masks = []
      self.process_sheet()
    except Exception as e:
      general_sheet_exception(self.SHEET_NAME, e)

  def process_sheet(self):
    general_params = True
    resolved_epochs = [None] * self.sheet.shape[1] 
    resolved_arms = [None] * self.sheet.shape[0] 
    for rindex, row in self.sheet.iterrows():
      key = self.read_cell(rindex, self.PARAMS_NAME_COL)
      if general_params:
        #print(f"KEY: {key}")
        if key in self.NAME_LABEL:
          self.name = self.read_cell(rindex, self.PARAMS_DATA_COL)
        elif key in self.LABEL_LABEL:
          self.label = self.read_cell(rindex, self.PARAMS_DATA_COL)
        elif key in self.DESCRIPTION_LABEL:
          self.description = self.read_cell(rindex, self.PARAMS_DATA_COL)
        elif key in self.TA_LABEL:
          self.therapeutic_areas = self.read_other_code_cell_mutiple(rindex, self.PARAMS_DATA_COL)
        elif key in self.RATIONALE_LABEL:
          self.rationale = self.read_cell(rindex, self.PARAMS_DATA_COL)
        elif key in self.BLINDING_LABEL:
          self.blinding = Alias.code(self.read_cdisc_klass_attribute_cell('StudyDesign', 'studyDesignBlindingScheme',rindex, self.PARAMS_DATA_COL), [])
        elif key in self.INTENT_LABEL:
          self.trial_intents = self.read_cdisc_klass_attribute_cell_multiple('StudyDesign', 'trialIntentType', rindex, self.PARAMS_DATA_COL)
        elif key in self.CHARACTERISTICS_LABEL:
          self.characteristics = self.read_cdisc_klass_attribute_cell_multiple('StudyDesign', 'characteristics', rindex, self.PARAMS_DATA_COL)
          #print(f"CHARAC: {self.characteristics}")
        elif key in self.TYPES_LABEL:
          self.trial_types = self.read_cdisc_klass_attribute_cell_multiple('StudyDesign', 'trialType', rindex, self.PARAMS_DATA_COL)
        elif key in self.INT_LABEL:
          self.intervention_model = self.read_cdisc_klass_attribute_cell('StudyDesign', 'interventionModel', rindex, self.PARAMS_DATA_COL)
        elif key in self.MAIN_TIMELINE_LABEL:
          #print(f"MAIN TL: {rindex}")
          self.main_timeline = self.read_cell(rindex, self.PARAMS_DATA_COL)
        elif key in self.OTHER_TIMELINES_LABEL:
          #print(f"OTHER TL: {rindex}")
          self.other_timelines = self.read_cell_multiple(rindex, self.PARAMS_DATA_COL)
        elif key in self.MASKING_ROLE_LABEL:
          #print(f"MASKING: {rindex}")
          self._set_masking(rindex, self.PARAMS_DATA_COL)
        elif key in '':
          general_params = False
          start_row = rindex + 1
          #print(f"START: {start_row}")
      else:
        for cindex in range(0, len(self.sheet.columns)):
          epoch_index = cindex - 1
          cell = self.read_cell(rindex, cindex)
          #print(f"ARMS EPOCHS: {rindex} = {cell}")
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
                
      self.double_link(self.epochs, 'previousId', 'nextId')

    study_design = self._create_design()
    self.study_designs.append(study_design)

  def _add_arm(self, name):
    arm = self.managers.cross_references.get(StudyArm, name)
    if arm is not None:
      if name not in self.arm_names:
        self.arm_names[name] = True
        self.arms.append(arm)
      return arm
    else:
      self._general_error(f"No arm definition found for arm '{name}'")
      return None

  def _add_epoch(self, name):
    epoch = self.managers.cross_references.get(StudyEpoch, name)
    if epoch is not None:
      if name not in self.epoch_names:
        self.epoch_names[name] = True
        self.epochs.append(epoch)
      return epoch
    else:
      self._general_error(f"No epoch definition found for epoch '{name}'")
      return None
  
  def _add_element(self, name):
    element = self.managers.cross_references.get(StudyElement, name)
    if element is not None:
      if name not in self.elements:
        self.elements[name] = element
      return element
    else:
      self._general_error(f"No element definition found for element '{name}'")
      return None

  def _add_cell(self, arm, epoch, elements):
    try:
      return StudyCell(
        id=self.managers.id_manager.build_id(StudyCell), 
        armId=arm,
        epochId=epoch,
        elementIds=elements
      )
    except Exception as e:
      self._general_error("Failed to create StudyCell object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      return None

  def _create_design(self):
    try:
      result = StudyDesign(
        id=self.managers.id_manager.build_id(StudyDesign), 
        name=self.name,
        description=self.description,
        label=self.label,
        trialIntentTypes=self.trial_intents, 
        trialTypes=self.trial_types, 
        interventionModel=self.intervention_model,
        studyCells=self.cells,
        arms=self.arms,
        epochs=self.epochs,
        elements=list(self.elements.values()),
        therapeuticAreas=self.therapeutic_areas,
        rationale=self.rationale, 
        blindingSchema=self.blinding, 
        contents=[],
        maskingRoles=self.masks,
        characteristics=self.characteristics
      )
      #print(f"SD: {result.characteristics}")
      return result
    except Exception as e:
      self._general_error("Failed to create StudyDesign object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      return None
  

  def _set_masking(self, rindex, cindex):
    if self.managers.option_manager.get(Options.USDM_VERSION) == '2':
      return None
    else:
      try:
        text = self.read_cell(rindex, cindex)
        parts = text.split('=')
        if len(parts) == 2: 
          code = CDISCCT(self.managers.cdisc_ct_library).code_for_attribute('Masking', 'role', parts[0].strip())
          if code:
            mask = Masking(id=self.managers.id_manager.build_id(Masking), description=parts[1].strip(), role=code)
            self.masks.append(mask)
            self.managers.cross_references.add(mask.id, mask)
            return mask
          else:
            self._error(rindex, cindex, f"Failed to decode masking role data '{text}', must be a valid role code '{parts[0]}'")
            return None
        else:
          self._error(rindex, cindex, f"Failed to decode masking role data '{text}', no '=' detected")
          return None
      except Exception as e:
        self._error(rindex, cindex, "Failed to create Masking object, exception {e}")
        self._traceback(f"{traceback.format_exc()}")
        return None
