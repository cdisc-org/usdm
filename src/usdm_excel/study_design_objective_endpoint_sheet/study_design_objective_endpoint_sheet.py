from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.objective import Objective
from usdm_model.endpoint import Endpoint

class StudyDesignObjectiveEndpointSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignOE')
      self.objectives = []
      current = None
      for index, row in self.sheet.iterrows():
        o_xref = self.read_cell_by_name(index, "objectiveXref")
        o_description = self.read_cell_by_name(index, 'objectiveDescription') # Note, dont use description read method, we need to know if really empty.
        e_xref = self.read_cell_by_name(index, "endpointXref")
        e_description = self.read_description_by_name(index, 'endpointDescription')
        e_p_description = self.read_description_by_name(index, 'endpointPurposeDescription')
        e_level = self.read_cdisc_klass_attribute_cell_by_name('Endpoint', 'endpointLevel', index, "endpointLevel")
        if not o_description == "":
          o_level = self.read_cdisc_klass_attribute_cell_by_name('Objective', 'objectiveLevel', index, "objectiveLevel")
          try:
            current = Objective(objectiveId=id_manager.build_id(Objective),
              objectiveDescription=o_description, 
              objectiveLevel=o_level,
              objectiveEndpoints=[]
            )
          except Exception as e:
            self._general_error(f"Failed to create Objective object, exception {e}")
          else:
            self.objectives.append(current)
            cross_references.add(o_xref, current.objectiveId)
        if current is not None:
          try:
            ep = Endpoint(endpointId=id_manager.build_id(Endpoint), 
              endpointDescription=e_description, 
              endpointPurposeDescription=e_p_description, 
              endpointLevel=e_level
            )  
          except Exception as e:
            self._general_error(f"Failed to create Endpoint object, exception {e}")
          else:
            current.objectiveEndpoints.append(ep)
            cross_references.add(e_xref, ep.endpointId)
        else:
          self._general_error("Failed to add Endpoint, no Objective set")

    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

