from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
import traceback
import pandas as pd
from usdm.indication import Indication
from usdm.investigational_intervention import InvestigationalIntervention

class StudyDesignIISheet(BaseSheet):

  def __init__(self, file_path, id_manager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignII'), id_manager)
      self.indications = []
      self.interventions = []
      for index, row in self.sheet.iterrows():
        xref = self.clean_cell(row, index, "xref")
        type = self.clean_cell(row, index, "type")
        description = self.clean_cell(row, index, "description")
        #codes = self._build_codes(row, index)
        codes = self.other_code_cell_mutiple(self.clean_cell(row, index, "codes"))
        if type.upper() == "IND":
          item = Indication(indicationId=self.id_manager.build_id(Indication), indicationDescription=description, codes=codes)
          self.indications.append(item)
          cross_references.add(xref, item.indicationId)
        else:
          item = InvestigationalIntervention(investigationalInterventionId=self.id_manager.build_id(InvestigationalIntervention), interventionDescription=description, codes=codes)
          self.interventions.append(item)
          cross_references.add(xref, item.investigationalInterventionId)        
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()

  # def _build_codes(self, row, index):
  #   result = []
  #   value = self.clean_cell(row, index, "codes")
  #   #print("CODE1:", value)
  #   items = value.split(",")
  #   for item in items:
  #     #print("CODE2:", item)
  #     code = self.other_code_cell(item)
  #     #print("CODE3:", code)
  #     if not code == None:
  #       result.append(code)
  #   return result