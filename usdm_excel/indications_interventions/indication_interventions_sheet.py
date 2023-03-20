from usdm_excel.base_sheet import BaseSheet
import traceback
import pandas as pd
from usdm.indication import Indication
from usdm.investigational_intervention import InvestigationalIntervention

class IndicationsInterventionsSheet(BaseSheet):

  def __init__(self, file_path, id_manager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignII'), id_manager)
      self.indications = []
      self.interventions = []
      for index, row in self.sheet.iterrows():
        type = self.clean_cell(row, index, "type")
        description = self.clean_cell(row, index, "description")
        codes = self._build_codes(row, index)
        if type.upper() == "IND":
          self.indications.append(Indication(indicationId=self.id_manager.build_id(Indication), indicationDescription=description, codes=codes))
        else:
          self.interventions.append(InvestigationalIntervention(investigationalInterventionId=self.id_manager.build_id(InvestigationalIntervention), interventionDescription=description, codes=codes))
        
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()

  def _build_codes(self, row, index):
    result = []
    value = self.clean_cell(row, index, "codes")
    #print("CODE1:", value)
    items = value.split(",")
    for item in items:
      #print("CODE2:", item)
      code = self.other_code_cell(item)
      #print("CODE3:", code)
      if not code == None:
        result.append(code)
    return result