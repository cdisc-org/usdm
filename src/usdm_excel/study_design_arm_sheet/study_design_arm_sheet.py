import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.study_arm import StudyArm
from usdm_excel.globals import Globals

class StudyDesignArmSheet(BaseSheet):

  SHEET_NAME = 'studyDesignArms'
  
  def __init__(self, file_path: str, globals: Globals):
    try:
      self.items = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME)
      for index, row in self.sheet.iterrows():
        name = self.read_cell_by_name(index, ['studyArmName', 'name'])
        description = self.read_cell_by_name(index, ['studyArmDescription', 'description'])
        label = self.read_cell_by_name(index, 'label', default="", must_be_present=False)
        arm_type = self.read_cdisc_klass_attribute_cell_by_name('StudyArm', 'studyArmType', index, ['studyArmType', 'type'])
        arm_origin_description = self.read_cell_by_name(index, ['studyArmDataOriginDescription', 'dataOriginDescription'])
        arm_origin_type = self.read_cdisc_klass_attribute_cell_by_name('StudyArm', 'studyArmDataOriginType', index, ['studyArmDataOriginType', 'dataOriginType'])
        try:
          item = StudyArm(
            id=self.globals.id_manager.build_id(StudyArm), 
            name=name,
            description=description,
            label=label,
            type=arm_type,
            dataOriginDescription=arm_origin_description,
            dataOriginType=arm_origin_type
          )
        except Exception as e:
          self._general_exception(f"Failed to create StudyArm object", e)
        else:
          self.items.append(item)
          self.globals.cross_references.add(name, item)     
    except Exception as e:
      self._sheet_exception(e)

