from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
from usdm_model.objective import Objective
from usdm_model.endpoint import Endpoint

import traceback

class StudyDesignObjectiveEndpointSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignOE')
      self.objectives = []
      current = None
      for index, row in self.sheet.iterrows():
        o_text = self.read_cell_by_name(index, 'objectiveText') 
        ep_name = self.read_cell_by_name(index, ['endpointXref', 'endpointName'])
        ep_description = self.read_description_by_name(index, 'endpointDescription')
        ep_label = self.read_cell_by_name(index, ["endpointLabel"], default='') 
        ep_text = self.read_cell_by_name(index, 'endpointText') 
        ep_purpose = self.read_cell_by_name(index, ['endpointPurposeDescription', 'endpointPurpose'], default='None provided')
        ep_level = self.read_cdisc_klass_attribute_cell_by_name('Endpoint', 'endpointLevel', index, "endpointLevel")
        if o_text:
          o_name = self.read_cell_by_name(index, ["objectiveXref", "objectiveName"]) 
          o_description = self.read_description_by_name(index, 'objectiveDescription')
          o_label = self.read_cell_by_name(index, ["objectiveLabel"], default='') 
          o_level = self.read_cdisc_klass_attribute_cell_by_name('Objective', 'objectiveLevel', index, "objectiveLevel")
          try:
            current = Objective(id=id_manager.build_id(Objective),
              instanceType="OBJECTIVE",
              name=o_name,
              description=o_description, 
              label=o_label,
              text=o_text,
              level=o_level,
              objectiveEndpoints=[]
            )
          except Exception as e:
            self._general_error(f"Failed to create Objective object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            self.objectives.append(current)
            cross_references.add(o_name, current)
        if current is not None:
          try:
            ep = Endpoint(id=id_manager.build_id(Endpoint),
              instanceType="ENDPOINT",
              name=ep_name,
              description=ep_description,
              label=ep_label,
              text=ep_text, 
              purpose=ep_purpose, 
              level=ep_level
            )  
          except Exception as e:
            self._general_error(f"Failed to create Endpoint object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            current.objectiveEndpoints.append(ep)
            cross_references.add(ep_name, ep)
        else:
          self._general_error("Failed to add Endpoint, no Objective set")

    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

