from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
from usdm_model.indication import Indication

import traceback

class StudyDesignIndicationSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignIndications')
      self.items = []
      for index, row in self.sheet.iterrows():
        name = self.read_cell_by_name(index, "name")
        description = self.read_cell_by_name(index, "description")
        label = self.read_cell_by_name(index, 'label', default="")
        rare = self.read_boolean_cell_by_name(index, 'isRareDisease', must_be_present=False)
        codes = self.read_other_code_cell_multiple_by_name(index, "codes")
        item = self.create_object(Indication, {'name': name, 'description': description, 'label': label, 'isRareDisease': rare, 'codes': codes})
        if item:
          self.items.append(item)
          cross_references.add(name, item)
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

