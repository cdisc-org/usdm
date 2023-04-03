from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.encounter import Encounter
from usdm_model.transition_rule import TransitionRule

class StudyDesignEncounterSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      #super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignEncounters'))
      super().__init__(file_path=file_path, sheet_name='studyDesignEncounters')
      self.items = []
      for index, row in self.sheet.iterrows():
        start_rule = None
        end_rule = None
        xref = self.clean_cell(row, index, 'xref')
        name = self.clean_cell(row, index, 'encounterName')
        description = self.clean_cell(row, index, 'encounterDescription')
        type = self.read_cdisc_klass_attribute_cell_by_name('Encounter', 'encounterType', index, 'encounterType')
        setting = self.read_cdisc_klass_attribute_cell_by_name('Encounter', 'encounterEnvironmentalSetting', index, 'encounterEnvironmentalSetting')
        modes = self.read_cdisc_klass_attribute_cell_by_name_multiple('Encounter', 'encounterContactModes', index, 'encounterContactModes')
        start_rule_text = self.clean_cell(row, index, 'transitionStartRule')
        end_rule_text = self.clean_cell(row, index, 'transitionEndRule')
        if not start_rule_text == "":
          start_rule = TransitionRule(transitionRuleId=id_manager.build_id(TransitionRule), transitionRuleDescription=start_rule_text)
        if not end_rule_text == "":
          end_rule = TransitionRule(transitionRuleId=id_manager.build_id(TransitionRule), transitionRuleDescription=end_rule_text)
        item = Encounter(
          encounterId=id_manager.build_id(Encounter), 
          encounterName=name,
          encounterDescription=description,
          encounterType=type, 
          encounterEnvironmentalSetting=setting,
          encounterContactModes=modes,
          transitionStartRule=start_rule,
          transitionEndRule=end_rule
        )
        self.items.append(item)
        cross_references.add(xref, item)     
      self.double_link(self.items, 'encounterId', 'previousEncounterId', 'nextEncounterId')   
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()
