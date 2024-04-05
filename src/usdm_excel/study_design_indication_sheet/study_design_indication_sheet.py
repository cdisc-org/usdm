import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.indication import Indication
from usdm_excel.managers import Managers

class StudyDesignIndicationSheet(BaseSheet):

  SHEET_NAME = 'studyDesignIndications'
  
  def __init__(self, file_path: str, managers: Managers):
    try:
      super().__init__(file_path=file_path, managers=managers, sheet_name=self.SHEET_NAME )
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
          self.managers.cross_references.add(name, item)
    except Exception as e:
      self._general_sheet_exception(e)

