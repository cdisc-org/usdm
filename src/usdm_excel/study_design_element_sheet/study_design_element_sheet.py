from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.study_element import StudyElement
from usdm_model.transition_rule import TransitionRule

class StudyDesignElementSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignElements')
      self.items = []
      for index, row in self.sheet.iterrows():
        start_rule = None
        end_rule = None
        xref = self.read_cell_by_name(index, 'xref', default="")
        name = self.read_cell_by_name(index, ['studyElementName', 'name'])
        description = self.read_cell_by_name(index, ['studyElementDescription', 'description'])
        label = self.read_cell_by_name(index, 'label', default="")
        start_rule_text = self.read_cell_by_name(index, 'transitionStartRule')
        end_rule_text = self.read_cell_by_name(index, 'transitionEndRule')
        if not start_rule_text == "":
          start_rule = TransitionRule(id=id_manager.build_id(TransitionRule), name=f"ELEMENT_START_RULE_{index + 1}", text=start_rule_text)
        if not end_rule_text == "":
          end_rule = TransitionRule(id=id_manager.build_id(TransitionRule), name=f"ELEMENT_END_RULE_{index + 1}", text=end_rule_text)
        try:
          item = StudyElement(
            id=id_manager.build_id(StudyElement), 
            name=name,
            description=description,
            label=label,
            transitionStartRule=start_rule,
            transitionEndRule=end_rule
          )
        except Exception as e:
          self._general_error(f"Failed to create StudyElement object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          self.items.append(item)
          cross_ref = xref if xref else name
          cross_references.add(cross_ref, item)     
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

