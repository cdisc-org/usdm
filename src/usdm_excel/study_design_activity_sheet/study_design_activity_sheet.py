from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.activity import Activity

class StudyDesignActivitySheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignActivities', optional=True)
      self.items = []
      if self.success:
        for index, row in self.sheet.iterrows():
          name = self.read_cell_by_name(index, ['activityName', 'name'])
          description = self.read_description_by_name(index, ['activityDescription', 'description'])
          label = self.read_cell_by_name(index, 'label', default="")
          conditional = self.read_boolean_cell_by_name(index, 'activityIsConditional')
          reason = self.read_cell_by_name(index, 'activityIsConditionalReason')
          try:
            item = Activity(
              id=id_manager.build_id(Activity), 
              name=name,
              description=description,
              label=label,
              activityIsConditional=conditional,
              activityIsConditionalReason=reason
            )
          except Exception as e:
            self._general_error(f"Failed to create Activity object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            self.items.append(item)
            cross_references.add(name, item)     
        self.double_link(self.items, 'previousActivityId', 'nextActivityId')   
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

