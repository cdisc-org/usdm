from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.procedure import Procedure

class StudyDesignProcedureSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignProcedures'))
      self.procedures = []
      for index, row in self.sheet.iterrows():
        xref = self.clean_cell(row, index, "xref")
        type = self.clean_cell(row, index, "procedureType")
        code = self.other_code_cell(self.clean_cell(row, index, 'procedureCode'))
        conditional = self.boolean_cell(self.clean_cell(row, index, 'procedureIsConditional'))
        reason = self.clean_cell(row, index, 'procedureIsConditionalReason')
        item = Procedure(procedureId=id_manager.build_id(Procedure), 
          procedureType=type, 
          procedureCode=code, 
          procedureIsConditional=conditional, 
          procedureIsConditionalReason=reason
        )
        self.procedures.append(item)
        cross_references.add(xref, item)        
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()
