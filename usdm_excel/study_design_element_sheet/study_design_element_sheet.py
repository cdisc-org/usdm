from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm.study_element import StudyElement
from usdm.transition_rule import TransitionRule

class StudyDesignElementSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignElements'))
      self.items = []
      for index, row in self.sheet.iterrows():
        start_rule = None
        end_rule = None
        xref = self.clean_cell(row, index, 'xref')
        name = self.clean_cell(row, index, 'studyElementName')
        description = self.clean_cell(row, index, 'studyElementDescription')
        start_rule_text = self.clean_cell(row, index, 'transitionStartRule')
        end_rule_text = self.clean_cell(row, index, 'transitionEndRule')
        if not start_rule_text == "":
          start_rule = TransitionRule(transitionRuleId=id_manager.build_id(TransitionRule), transitionRuleDescription=start_rule_text)
        if not end_rule_text == "":
          end_rule = TransitionRule(transitionRuleId=id_manager.build_id(TransitionRule), transitionRuleDescription=end_rule_text)
        item = StudyElement(
          studyElementId=id_manager.build_id(StudyElement), 
          studyElementName=name,
          studyElementDescription=description,
          transitionStartRule=start_rule,
          transitionEndRule=end_rule
        )
        self.items.append(item)
        cross_references.add(xref, item)     
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()
