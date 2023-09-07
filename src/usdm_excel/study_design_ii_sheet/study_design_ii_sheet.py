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
      super().__init__(file_path=file_path, sheet_name='studyDesignII')
      self.indications = []
      self.interventions = []
      for index, row in self.sheet.iterrows():
        xref = self.read_cell_by_name(index, ["xref", "name"])
        type = self.read_cell_by_name(index, "type")
        description = self.read_description_by_name(index, "description")
        label = self.read_cell_by_name(index, 'label', default="")
        codes = self.read_other_code_cell_multiple_by_name(index, "codes")
        if type.upper() == "IND":
          try:
            item = Indication(id=id_manager.build_id(Indication), name=xref, description=description, label=label, codes=codes)
          except Exception as e:
            self._general_error(f"Failed to create Indication object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            self.indications.append(item)
            cross_references.add(xref, item)
        else:
          try:
            item = InvestigationalIntervention(id=id_manager.build_id(InvestigationalIntervention), description=description, codes=codes)
          except Exception as e:
            self._general_error(f"Failed to create InvestigationalIntervention object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            self.interventions.append(item)
            cross_references.add(xref, item)        
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

