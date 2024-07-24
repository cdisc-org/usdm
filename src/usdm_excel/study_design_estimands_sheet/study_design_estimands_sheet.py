from usdm_excel.base_sheet import BaseSheet
#from usdm_excel.cross_ref import cross_references
#from usdm_excel.id_manager import id_manager
import traceback
from usdm_model.intercurrent_event import IntercurrentEvent
from usdm_model.analysis_population import AnalysisPopulation
from usdm_model.estimand import Estimand
from usdm_model.study_intervention import StudyIntervention
from usdm_model.endpoint import Endpoint
from usdm_excel.globals import Globals

class StudyDesignEstimandsSheet(BaseSheet):

  SHEET_NAME = 'studyDesignEstimands'
  
  def __init__(self, file_path: str, globals: Globals):
    try:
      self.estimands = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME)
      current = None
      current_ice_name = None
      current_ice_description = None
      for index, row in self.sheet.iterrows():
        e_summary = self.read_cell_by_name(index, "summaryMeasure")
        ap_description = self.read_cell_by_name(index, 'populationDescription')
        ice_name = self.read_cell_by_name(index, ['intercurrentEventName', 'name'])
        ice_description = self.read_cell_by_name(index, ['intercurrentEventDescription', 'description'])
        ice_label = self.read_cell_by_name(index, 'label', must_be_present=False)
        ice_strategy = self.read_cell_by_name(index, "intercurrentEventStrategy")
        treatment_xref = self.read_cell_by_name(index, "treatmentXref")
        endpoint_xref = self.read_cell_by_name(index, "endpointXref")
        if not e_summary == "":
          try:
            ap = AnalysisPopulation(id=self.globals.id_manager.build_id(AnalysisPopulation), name=f"AP_{index+1}", text=ap_description) 
          except Exception as e:
            self._general_error(f"Failed to create AnalysisPopulation object", e)
          else:
            try:
              treatment_id = self._get_treatment(treatment_xref)
              endpoint_id = self._get_endpoint(endpoint_xref)
              current = Estimand(id=self.globals.id_manager.build_id(Estimand), summaryMeasure=e_summary, analysisPopulation=ap, interventionId=treatment_id, variableOfInterestId=endpoint_id, intercurrentEvents=[])
            except Exception as e:
              self._general_error(f"Failed to create Estimand object", e)
            else:
              self.estimands.append(current)  
        if current is not None:
          try:
            ice_name = current_ice_name if ice_name == "" else ice_name
            ice_description = current_ice_description if ice_description == "" else ice_description
            ice = IntercurrentEvent(id=self.globals.id_manager.build_id(IntercurrentEvent), name=ice_name, description=ice_description, label=ice_label, strategy=ice_strategy)
            current_ice_name = ice_name
            current_ice_description = ice_description
          except Exception as e:
            self._general_error(f"Failed to create IntercurrentEvent object", e)
          else:
            current.intercurrentEvents.append(ice)
        else:
          self._general_error("Failed to add IntercurrentEvent, no Estimand set")

    except Exception as e:
      self._sheet_exception(e)

  def _get_treatment(self, name):
    return self._get_cross_reference(StudyIntervention, name, 'study intervention')

  def _get_endpoint(self, name):
    return self._get_cross_reference(Endpoint, name, 'endpoint')
