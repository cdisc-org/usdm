from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.encounter import Encounter
from usdm_model.transition_rule import TransitionRule
from usdm_model.timing import Timing

class StudyDesignEncounterSheet(BaseSheet):

  def __init__(self, file_path, manager):
    try:
      super().__init__(file_path=file_path, manager=manager, sheet_name='studyDesignEncounters')
      self.items = []
      for index, row in self.sheet.iterrows():
        start_rule = None
        end_rule = None
        xref = self.read_cell_by_name(index, 'xref', must_be_present=False)
        name = self.read_cell_by_name(index, ['encounterName', 'name'])
        description = self.read_cell_by_name(index, ['encounterDescription', 'description'])
        label = self.read_cell_by_name(index, 'label', default='', must_be_present=False)
        type = self.read_cdisc_klass_attribute_cell_by_name('Encounter', 'encounterType', index, ['encounterType', 'type'])
        settings = self.read_cdisc_klass_attribute_cell_multiple_by_name('Encounter', 'encounterEnvironmentalSetting', index, ['encounterEnvironmentalSetting', 'environmentalSetting'])
        modes = self.read_cdisc_klass_attribute_cell_multiple_by_name('Encounter', 'encounterContactModes', index, ['encounterContactModes', 'contactModes'])
        start_rule_text = self.read_cell_by_name(index, 'transitionStartRule')
        end_rule_text = self.read_cell_by_name(index, 'transitionEndRule')
        timing_xref = self.read_cell_by_name(index, 'window', must_be_present=False)
        if start_rule_text:
          start_rule = TransitionRule(id=self.managers.id_manager.build_id(TransitionRule), name=f"ENCOUNTER_START_RULE_{index + 1}", text=start_rule_text)
        if end_rule_text:
          end_rule = TransitionRule(id=self.managers.id_manager.build_id(TransitionRule), name=f"ENCOUNTER_START_RULE_{index + 1}", text=end_rule_text)
        if timing_xref:
          timing = self.managers.cross_references.get(Timing, timing_xref)
          timing_id = timing.id if timing else None
        else:
          timing_id = None
        try:
          item = Encounter(
            id=self.managers.id_manager.build_id(Encounter), 
            name=name,
            description=description,
            label=label,
            type=type, 
            environmentalSetting=settings,
            contactModes=modes,
            transitionStartRule=start_rule,
            transitionEndRule=end_rule,
            scheduledAtId=timing_id
          )
        except Exception as e:
          self._general_error(f"Failed to create Encounter object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          self.items.append(item)
          cross_ref = xref if xref else name
          self.managers.cross_references.add(cross_ref, item)     
      self.double_link(self.items, 'previousId', 'nextId')   
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

