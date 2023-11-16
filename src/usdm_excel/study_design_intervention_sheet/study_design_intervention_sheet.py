from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.indication import Indication
from usdm_model.study_intervention import StudyIntervention

class StudyDesignInterventionSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignInterventions')
      self.indications = []
      self.interventions = []
      for index, row in self.sheet.iterrows():
        name = self.read_cell_by_name(index, ["name"])
        description = self.read_description_by_name(index, "description")
        label = self.read_cell_by_name(index, 'label', default="")
        codes = self.read_other_code_cell_multiple_by_name(index, "codes")
        try:
          item = StudyIntervention(id=id_manager.build_id(StudyIntervention), name=name, description=description, label=label, codes=codes)
        except Exception as e:
          self._general_error(f"Failed to create StudyIntervention object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          self.interventions.append(item)
          cross_references.add(name, item)        
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

