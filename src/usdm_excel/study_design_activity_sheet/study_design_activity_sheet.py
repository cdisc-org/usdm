import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.activity import Activity
from usdm_excel.globals import Globals

class StudyDesignActivitySheet(BaseSheet):

  SHEET_NAME = 'studyDesignActivities'

  def __init__(self, file_path: str, globals: Globals):
    try:
      self.items = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME, optional=True)
      if self.success:
        for index, row in self.sheet.iterrows():
          name = self.read_cell_by_name(index, ['activityName', 'name'])
          description = self.read_cell_by_name(index, ['activityDescription', 'description'])
          label = self.read_cell_by_name(index, 'label', default="", must_be_present=False)
          try:
            item = Activity(
              id=self.globals.id_manager.build_id(Activity), 
              name=name,
              description=description,
              label=label
            )
          except Exception as e:
            self._general_exception(f"Failed to create Activity object", e)
          else:
            self.items.append(item)
            self.globals.cross_references.add(name, item)     
        self.double_link(self.items, 'previousId', 'nextId')   
    except Exception as e:
      self._sheet_exception(e)

