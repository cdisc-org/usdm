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
      #super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignElements'))
      super().__init__(file_path=file_path, sheet_name='studyDesignElements')
      self.items = []
      for index, row in self.sheet.iterrows():
        start_rule = None
        end_rule = None
        xref = self.read_cell_by_name(index, 'xref')
        name = self.read_cell_by_name(index, 'studyElementName')
        description = self.read_description_by_name(index, 'studyElementDescription')
        start_rule_text = self.read_cell_by_name(index, 'transitionStartRule')
        end_rule_text = self.read_cell_by_name(index, 'transitionEndRule')
        if not start_rule_text == "":
          start_rule = TransitionRule(id=id_manager.build_id(TransitionRule), transitionRuleDescription=start_rule_text)
        if not end_rule_text == "":
          end_rule = TransitionRule(id=id_manager.build_id(TransitionRule), transitionRuleDescription=end_rule_text)
        try:
          item = StudyElement(
            i=id_manager.build_id(StudyElement), 
            studyElementName=name,
            studyElementDescription=description,
            transitionStartRule=start_rule,
            transitionEndRule=end_rule
          )
        except Exception as e:
          self._general_error(f"Failed to create StudyElement object, exception {e}")
        else:
          self.items.append(item)
          cross_references.add(xref, item)     
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

