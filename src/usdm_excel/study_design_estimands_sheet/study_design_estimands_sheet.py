from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.intercurrent_event import IntercurrentEvent
from usdm_model.analysis_population import AnalysisPopulation
from usdm_model.estimand import Estimand
from usdm_excel.cdisc_ct_library import cdisc_ct_library
from usdm_excel.cdisc_ct import CDISCCT

class StudyDesignEstimandsSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignEstimands')
      self.estimands = []
      current = None
      for index, row in self.sheet.iterrows():
        e_summary = self.read_cell_by_name(index, "summaryMeasure")
        ap_description = self.read_description_by_name(index, 'populationDescription')
        ice_name = self.read_cell_by_name(index, "intercurrentEventName")
        ice_description = self.read_description_by_name(index, 'intercurrentEventDescription')
        ice_strategy = self.read_cell_by_name(index, "intercurrentEventStrategy")
        treatment_xref = self.read_cell_by_name(index, "treatmentXref")
        treatment_id = cross_references.get(treatment_xref)
        endpoint_xref = self.read_cell_by_name(index, "endpointXref")
        endpoint_id = cross_references.get(endpoint_xref)
        if not e_summary == "":
          try:
            ap = AnalysisPopulation(id=id_manager.build_id(AnalysisPopulation), populationDescription=ap_description) 
          except Exception as e:
            self._general_error(f"Failed to create AnalysisPopulation object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            try:
              current = Estimand(id=id_manager.build_id(Estimand), summaryMeasure=e_summary, analysisPopulation=ap, treatment=treatment_id, variableOfInterest=endpoint_id, intercurrentEvents=[])
            except Exception as e:
              self._general_error(f"Failed to create Estimand object, exception {e}")
              self._traceback(f"{traceback.format_exc()}")
            else:
              self.estimands.append(current)  
        if current is not None:
          try:
            ice = IntercurrentEvent(id=id_manager.build_id(IntercurrentEvent), intercurrentEventName=ice_name, intercurrentEventDescription=ice_description, intercurrentEventStrategy=ice_strategy)
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
      self._traceback(f"{traceback.format_exc()}")

