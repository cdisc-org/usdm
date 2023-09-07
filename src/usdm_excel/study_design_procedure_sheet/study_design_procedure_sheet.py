from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.procedure import Procedure

class StudyDesignProcedureSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignProcedures')
      self.procedures = []
      for index, row in self.sheet.iterrows():
        xref = self.read_cell_by_name(index, "xref")
        name = self.read_cell_by_name(index, ["procedureName", 'name'])
        description = self.read_description_by_name(index, ['procedureDescription', 'description'])
        label = self.read_cell_by_name(index, 'label', default="")
        type = self.read_cell_by_name(index, "procedureType")
        code = self.read_other_code_cell_by_name(index, ['procedureCode', 'code'])
        conditional = self.read_boolean_cell_by_name(index, 'procedureIsConditional')
        reason = self.read_cell_by_name(index, 'procedureIsConditionalReason')
        try:
          item = Procedure(id=id_manager.build_id(Procedure),
            name=name,
            description=description,
            label=label,
            procedureType=type, 
            code=code, 
            procedureIsConditional=conditional, 
            procedureIsConditionalReason=reason
          )
        except Exception as e:
          self._general_error(f"Failed to create Procedure object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          self.procedures.append(item)
          cross_references.add(xref, item)        
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")
