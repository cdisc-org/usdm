from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
from usdm_model.intercurrent_event import IntercurrentEvent
from usdm_model.analysis_population import AnalysisPopulation
from usdm_model.estimand import Estimand
from usdm_model.investigational_intervention import InvestigationalIntervention
from usdm_model.endpoint import Endpoint

class StudyDesignEstimandsSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignEstimands')
      self.estimands = []
      current = None
      current_ice_name = None
      current_ice_description = None
      for index, row in self.sheet.iterrows():
        e_summary = self.read_cell_by_name(index, "summaryMeasure")
        ap_description = self.read_description_by_name(index, 'populationDescription')
        ice_name = self.read_cell_by_name(index, ['intercurrentEventName', 'name'])
        ice_description = self.read_description_by_name(index, ['intercurrentEventDescription', 'description'])
        ice_label = self.read_cell_by_name(index, 'label', default='')
        ice_strategy = self.read_cell_by_name(index, "intercurrentEventStrategy")
        treatment_xref = self.read_cell_by_name(index, "treatmentXref")
        endpoint_xref = self.read_cell_by_name(index, "endpointXref")
        if not e_summary == "":
          try:
            ap = AnalysisPopulation(id=id_manager.build_id(AnalysisPopulation), description=ap_description) 
          except Exception as e:
            self._general_error(f"Failed to create AnalysisPopulation object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            try:
              treatment = cross_references.get(InvestigationalIntervention, treatment_xref)
              endpoint = cross_references.get(Endpoint, endpoint_xref)
              treatment_id = treatment.id
              endpoint_id = endpoint.id
              current = Estimand(id=id_manager.build_id(Estimand), summaryMeasure=e_summary, analysisPopulation=ap, treatmentId=treatment_id, variableOfInterestId=endpoint_id, intercurrentEvents=[])
            except Exception as e:
              self._general_error(f"Failed to create Estimand object, exception {e}")
              self._traceback(f"{traceback.format_exc()}")
            else:
              self.estimands.append(current)  
        if current is not None:
          try:
            ice_name = current_ice_name if ice_name == "" else ice_name
            ice_description = current_ice_description if ice_description == "" else ice_description
            ice = IntercurrentEvent(id=id_manager.build_id(IntercurrentEvent), name=ice_name, description=ice_description, label=ice_label, intercurrentEventStrategy=ice_strategy)
            current_ice_name = ice_name
            current_ice_description = ice_description
          except Exception as e:
            self._general_error(f"Failed to create IntercurrentEvent object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            current.intercurrentEvents.append(ice)
        else:
          self._general_error("Failed to add IntercurrentEvent, no Estimand set")
          self._traceback(f"{traceback.format_exc()}")

    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      #print(f"{traceback.format_exc()}")
      self._traceback(f"{traceback.format_exc()}")

