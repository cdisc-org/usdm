import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.study_epoch import StudyEpoch
from usdm_excel.globals import Globals

class StudyDesignEpochSheet(BaseSheet):

  SHEET_NAME = 'studyDesignEpochs'
  
  def __init__(self, file_path: str, globals: Globals):
    try:
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME)
      self.items = []
      for index, row in self.sheet.iterrows():
        name = self.read_cell_by_name(index, ['studyEpochName', 'name'])
        description = self.read_cell_by_name(index, ['studyEpochDescription', 'description'])
        label = self.read_cell_by_name(index, 'label', default="", must_be_present=False)
        epoch_type = self.read_cdisc_klass_attribute_cell_by_name('StudyEpoch', 'studyEpochType', index, ['studyEpochType', 'type'])
        try:
          item = StudyEpoch(
            id=self.globals.id_manager.build_id(StudyEpoch), 
            name=name, 
            description=description,
            label=label,
            type=epoch_type
          )
        except Exception as e:
          self._general_exception(f"Failed to create StudyEpoch object", e)
        else:
          self.items.append(item)
          self.globals.cross_references.add(name, item)     
    except Exception as e:
      self._sheet_exception(e)