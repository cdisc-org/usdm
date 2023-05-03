from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.indication import Indication
from usdm_model.investigational_intervention import InvestigationalIntervention

class StudyDesignIISheet(BaseSheet):

  def __init__(self, file_path):
    try:
      #super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignII'))
      super().__init__(file_path=file_path, sheet_name='studyDesignII')
      self.indications = []
      self.interventions = []
      for index, row in self.sheet.iterrows():
        xref = self.read_cell_by_name(index, "xref")
        type = self.read_cell_by_name(index, "type")
        description = self.read_description_by_name(index, "description")
        #codes = self._build_codes(row, index)
        codes = self.read_other_code_cell_multiple_by_name(index, "codes")
        if type.upper() == "IND":
          item = Indication(indicationId=id_manager.build_id(Indication), indicationDescription=description, codes=codes)
          self.indications.append(item)
          cross_references.add(xref, item.indicationId)
        else:
          item = InvestigationalIntervention(investigationalInterventionId=id_manager.build_id(InvestigationalIntervention), interventionDescription=description, codes=codes)
          self.interventions.append(item)
          cross_references.add(xref, item.investigationalInterventionId)        
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

