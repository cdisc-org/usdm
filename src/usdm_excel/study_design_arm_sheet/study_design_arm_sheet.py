from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
from usdm_model.study_arm import StudyArm
import traceback

class StudyDesignArmSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignArms')
      self.items = []
      for index, row in self.sheet.iterrows():
        name = self.read_cell_by_name(index, 'studyArmName')
        description = self.read_cell_by_name(index, 'studyArmDescription')
        arm_type = self.read_cdisc_klass_attribute_cell_by_name('StudyArm', 'studyArmType', index, 'studyArmType')
        arm_origin_description = self.read_cell_by_name(index, 'studyArmDataOriginDescription')
        arm_origin_type = self.read_cdisc_klass_attribute_cell_by_name('StudyArm', 'studyArmDataOriginType', index, 'studyArmDataOriginType')
        item = StudyArm(
          studyArmId=id_manager.build_id(StudyArm), 
          studyArmName=name,
          studyArmDescription=description,
          studyArmType=arm_type,
          studyArmDataOriginDescription=arm_origin_description,
          studyArmDataOriginType=arm_origin_type
        )
        self.items.append(item)
        cross_references.add(name, item)     
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

