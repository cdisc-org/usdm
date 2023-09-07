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
        o_description = self.read_cell_by_name(index, 'objectiveDescription') # Note, dont use description read method, we need to know if really empty.
        e_xref = self.read_cell_by_name(index, ['endpointXref', 'endpointName'])
        ep_description = self.read_description_by_name(index, 'endpointDescription')
        ep_purpose = self.read_description_by_name(index, 'endpointPurposeDescription')
        if not ep_purpose:
          ep_purpose = "None provided" # Temp fix
        e_level = self.read_cdisc_klass_attribute_cell_by_name('Endpoint', 'endpointLevel', index, "endpointLevel")
        if not o_description == "":
          o_xref = self.read_cell_by_name(index, ["objectiveXref", "objectiveName"]) 
          o_label = self.read_cell_by_name(index, ["objectiveLabel"], default='') 
          o_level = self.read_cdisc_klass_attribute_cell_by_name('Objective', 'objectiveLevel', index, "objectiveLevel")
          try:
            current = Objective(id=id_manager.build_id(Objective),
              name=o_xref,
              description=o_description, 
              label=o_label,
              objectiveLevel=o_level,
              objectiveEndpoints=[]
            )
          except Exception as e:
            self._general_error(f"Failed to create Objective object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            self.objectives.append(current)
            cross_references.add(o_xref, current)
        if current is not None:
          try:
            ep = Endpoint(id=id_manager.build_id(Endpoint), 
              description=ep_description, 
              purpose=ep_purpose, 
              endpointLevel=e_level
            )  
          except Exception as e:
            self._general_error(f"Failed to create Endpoint object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            current.objectiveEndpoints.append(ep)
            cross_references.add(e_xref, ep)
        else:
          self._general_error("Failed to add Endpoint, no Objective set")

    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

