from usdm_excel.base_sheet import BaseSheet
import traceback
import pandas as pd
from usdm.objective import Objective
from usdm.endpoint import Endpoint
from usdm_excel.cdisc_ct_library import cdisc_ct_library

class StudyDesignObjectiveEndpointSheet(BaseSheet):

  def __init__(self, file_path, id_manager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignOE'), id_manager)
      self.objectives = []
      current = None
      for index, row in self.sheet.iterrows():
        o_description = self.clean_cell(row, index, "objectiveDescription")
        o_level = cdisc_ct_library.klass_and_attribute('StudyObjective', 'objectiveLevel', self.clean_cell(row, index, "objectiveLevel"))
        e_description = self.clean_cell(row, index, "endpointDescription")
        e_p_description = self.clean_cell(row, index, "endpointPurposeDescription")
        e_level = cdisc_ct_library.klass_and_attribute('StudyObjective', 'endpointLevel', self.clean_cell(row, index, "endpointLevel"))
        if not o_description == "":
          current = Objective(objectiveId=self.id_manager.build_id(Objective),
            objectiveDescription=o_description, 
            objectiveLevel=o_level,
            objectiveEndpoints=[]
          )
          self.objectives.append(current)
        ep = Endpoint(endpointId=self.id_manager.build_id(Endpoint), endpointDescription=e_description, endpointPurposeDescription=e_p_description, endpointLevel=e_level)  
        current.objectiveEndpoints.append(ep)
        
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()
