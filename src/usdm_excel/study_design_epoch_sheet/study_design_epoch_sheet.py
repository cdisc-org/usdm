from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
from usdm_model.study_epoch import StudyEpoch
import traceback

class StudyDesignEpochSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignEpochs')
      self.items = []
      for index, row in self.sheet.iterrows():
        name = self.read_cell_by_name(index, ['studyEpochName', 'name'])
        description = self.read_description_by_name(index, ['studyEpochDescription', 'description'])
        label = self.read_cell_by_name(index, 'label', default="")
        epoch_type = self.read_cdisc_klass_attribute_cell_by_name('StudyEpoch', 'studyEpochType', index, ['studyEpochType', 'type'])
        try:
          item = StudyEpoch(
            id=id_manager.build_id(StudyEpoch), 
            name=name, 
            description=description,
            label=label,
            type=epoch_type
          )
        except Exception as e:
          self._general_error(f"Failed to create StudyEpoch object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          self.items.append(item)
          cross_references.add(name, item)     
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")