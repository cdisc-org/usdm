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
      super().__init__(file_path=file_path, sheet_name='studyDesignEncounters')
      self.items = []
      for index, row in self.sheet.iterrows():
        start_rule = None
        end_rule = None
        xref = self.read_cell_by_name(index, 'xref')
        name = self.read_cell_by_name(index, ['encounterName', 'name'])
        description = self.read_description_by_name(index, ['encounterDescription', 'description'])
        label = self.read_cell_by_name(index, 'label', default='')
        type = self.read_cdisc_klass_attribute_cell_by_name('Encounter', 'encounterType', index, ['encounterType', 'type'])
        setting = self.read_cdisc_klass_attribute_cell_by_name('Encounter', 'encounterEnvironmentalSetting', index, 'encounterEnvironmentalSetting')
        modes = self.read_cdisc_klass_attribute_cell_multiple_by_name('Encounter', 'encounterContactModes', index, 'encounterContactModes')
        start_rule_text = self.read_cell_by_name(index, 'transitionStartRule')
        end_rule_text = self.read_cell_by_name(index, 'transitionEndRule')
        if not start_rule_text == "":
          start_rule = TransitionRule(id=id_manager.build_id(TransitionRule), description=start_rule_text)
        if not end_rule_text == "":
          end_rule = TransitionRule(id=id_manager.build_id(TransitionRule), description=end_rule_text)
        try:
          item = Encounter(
            id=id_manager.build_id(Encounter), 
            name=name,
            description=description,
            label=label,
            type=type, 
            encounterEnvironmentalSetting=setting,
            encounterContactModes=modes,
            transitionStartRule=start_rule,
            transitionEndRule=end_rule
          )
        except Exception as e:
          self._general_error(f"Failed to create Encounter object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          self.items.append(item)
          cross_references.add(xref, item)     
      self.double_link(self.items, 'previousEncounterId', 'nextEncounterId')   
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

