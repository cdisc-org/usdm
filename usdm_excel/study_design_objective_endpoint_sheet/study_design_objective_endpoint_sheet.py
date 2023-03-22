from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
import traceback
import pandas as pd
from usdm.objective import Objective
from usdm.endpoint import Endpoint
from usdm_excel.cdisc_ct_library import cdisc_ct_library
from usdm_excel.cdisc_ct import CDISCCT

class StudyDesignObjectiveEndpointSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignOE'))
      self.objectives = []
      current = None
      for index, row in self.sheet.iterrows():
        o_xref = self.clean_cell(row, index, "objectiveXref")
        o_description = self.clean_cell(row, index, "objectiveDescription")
        o_level = cdisc_ct_library.klass_and_attribute('Objective', 'objectiveLevel', self.clean_cell(row, index, "objectiveLevel"))
        e_xref = self.clean_cell(row, index, "endpointXref")
        e_description = self.clean_cell(row, index, "endpointDescription")
        e_p_description = self.clean_cell(row, index, "endpointPurposeDescription")
        e_level = cdisc_ct_library.klass_and_attribute('Endpoint', 'endpointLevel', self.clean_cell(row, index, "endpointLevel"))
        if not o_description == "":
          current = Objective(objectiveId=id_manager.build_id(Objective),
            objectiveDescription=o_description, 
            objectiveLevel=CDISCCT().code(code=o_level['conceptId'], decode=o_level['preferredTerm']),
            objectiveEndpoints=[]
          )
          self.objectives.append(current)
          cross_references.add(o_xref, current.objectiveId)
        ep = Endpoint(endpointId=id_manager.build_id(Endpoint), 
          endpointDescription=e_description, 
          endpointPurposeDescription=e_p_description, 
          endpointLevel=CDISCCT().code(code=e_level['conceptId'], decode=e_level['preferredTerm'])
        )  
        current.objectiveEndpoints.append(ep)
        cross_references.add(e_xref, ep.endpointId)
        
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()
